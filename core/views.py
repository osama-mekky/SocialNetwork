from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render ,redirect




from django.views.generic.edit import CreateView ,UpdateView
from django.views.generic.list import ListView
from .models import *
from django.contrib.auth import authenticate ,login , logout

#to can not allow any person acheve the prfile page without login 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .forms import *

from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,'home.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'GET':
            return render(request,'login.html')
        elif request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else :
                messages.error(request,"Username or password in invailed")
                return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('login')        


class singupView(CreateView):
    model=User
    form_class = SignupForm
    template_name = 'singup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('profile')
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super(singupView,self).get(*args,**kwargs)


# @login_required(login_url='login')
# def profile(request):
#     return render(request,"profile.html") 

@method_decorator(login_required(login_url='login'),name='dispatch')
class Profile(ListView):
    model=Post
    template_name = 'profile.html'
    #paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(user = self.request.user).order_by('-date_created')
    
    


@method_decorator(login_required(login_url='login'),name='dispatch')
class AccountSettingsView(UpdateView):
    model =User
    fields = ["first_name","last_name","profile_pic","bio"]
    template_name = 'account_settings.html'
    #after enter save 
    success_url ='/profile'

    def get_object(self, queryset= None ):
        return self.request.user
    

@method_decorator(login_required(login_url='login'),name='dispatch')
class CreatePost(CreateView):
    model = Post
    fields = ['caption']
    template_name = 'new_post.html'
    success_url = '/profile'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    


@method_decorator(login_required(login_url='login'),name='dispatch')
class FriendProfile(ListView):
    model=Post
    template_name = 'friend_profile.html'
    #paginate_by = 5

    def get_queryset(self):
        friend_username = self.kwargs['username']
        friend = User.objects.get(username = friend_username)
        return Post.objects.filter(user = friend).order_by('-date_created')
    
    def get(self,request,*args, **kwargs) :
        friend_username = self.kwargs['username']
        user_username = self.request.user.username
        if friend_username == user_username:
            return redirect('profile')
        else :
            return super(FriendProfile,self).get(request,*args,**kwargs)


    #to show detiales profile my frined
    def get_context_data(self,*, object_list=None,**kwargs):
        context= super().get_context_data(**kwargs)
        friend_username = self.kwargs['username']
        friend = User.objects.get(username = friend_username)
        context['friend'] = friend
        #follow button
        is_following = self.request.user.is_following(friend)
        context['is_following'] = is_following
        return context

    #becaues when you typing the username of me the page open without follow or unfollwo
 
        


#button of search 
@method_decorator(login_required(login_url='login'),name='dispatch')
class SearchResults(ListView):
    model = User
    template_name = 'search_results.html'
    paginate_by = 5


    def get_queryset(self):
        search_term = self.request.GET['search-term']
        qs= User.objects.filter(username__contains=search_term)
        return qs
    


#run the follow fenctiontly
@login_required(login_url='login')
def follow_user(request,id):
    user_A = request.user
    user_B = User.objects.get(id=id)
    new_friend = Friend(user_A = user_A ,user_B=user_B)
    new_friend.save()
    return redirect('/user/'+user_B.username)


#run the unfollow fenctiontly
@login_required(login_url='login')
def unfollow_user(request,id):
    user_A = request.user
    user_B = User.objects.get(id=id)
    Friend.objects.filter(user_A=user_A,user_B=user_B).delete()
    return redirect('/user/'+user_B.username)
     

#####################################
@method_decorator(login_required(login_url='login'),name='dispatch')
class HomePage(ListView):
    model = Post
    template_name = 'Home.html'
    #paginate_by = 5   

    #funtion return all users im following him
    def get_queryset(self):
        followings =self.request.user.get_follwoings()
        return Post.objects.filter(user_id__in=followings).order_by('-date_created')
