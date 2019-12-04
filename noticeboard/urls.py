"""noticeboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from groups import views as group_views
from posts import views as post_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', user_views.login, name='login'),
    path('api/signup/', user_views.signup, name='signup'),
    path('api/create_group/', group_views.create_group, name='create_group'),
    path('api/add_member/', group_views.add_member, name='add_member'),
    path('api/user_groups/', group_views.user_groups, name='user_groups'),
    path('api/group_members/', group_views.group_members, name='group_members'),
    path('api/create_post/', post_views.create_post, name='create_post'),
    path('api/share_to_group/', post_views.share_to_group, name='share_to_group'),
    path('api/get_group_posts/', post_views.get_group_posts, name='get_group_posts'),
    path('api/get_user_posts/', post_views.get_user_posts, name='get_user_posts'),
    path('api/get_post/', post_views.get_post, name='get_post'),
    path('api/get_my_posts/', post_views.get_my_posts, name='get_my_posts'),
    path('api/get_group_details/', group_views.get_group_details, name='get_group_details'),
]
