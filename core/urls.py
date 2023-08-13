from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
    path('',views.HomePage.as_view(),name='home'),
    path('login',views.login_page,name='login'),
    path('singup',views.singupView.as_view(),name='singup'),
    path('profile',views.Profile.as_view(),name='profile'),
    path('logout',views.logout_user,name='logout'),
    path('account_settings',views.AccountSettingsView.as_view(),name='account_settings'),
    path('new_post',views.CreatePost.as_view(),name='new_post'),
    path('user/<str:username>',views.FriendProfile.as_view(),name='friend_profile'),
    path('search',views.SearchResults.as_view(),name='search'),
    path('follow/<int:id>',views.follow_user,name='follow_user'),
    path('unfollow/<int:id>',views.unfollow_user,name='unfollow_user'),
]