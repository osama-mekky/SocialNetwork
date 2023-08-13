# Generated by Django 3.2.4 on 2023-08-08 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_A', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_A', to=settings.AUTH_USER_MODEL)),
                ('user_B', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_B', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
