from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *

from groups.models import Groups, TimeOfJoining
from posts.models import Posts, PostGroupSharing, PostUserSharing
from users.models import CustomUser


@api_view(['POST'])
def create_post(request):
    user = request.user
    title = request.data.get('title')
    content = request.data.get('content')
    if not title:
        return Response({'error': 'Title field is empty'}, status=HTTP_400_BAD_REQUEST)
    post = Posts.objects.create(title=title, content=content, author=user)
    return Response({'message': 'Post created successfully'}, status=HTTP_200_OK)


@api_view(['POST'])
def share_to_group(request):
    user = request.user
    group_id = request.data.get('group_id')
    post_id = request.data.get('post_id')
    if not group_id or post_id:
        return Response({'error': 'Group id or post id not provided'}, status=HTTP_400_BAD_REQUEST)
    group = Groups.objects.filter(id=group_id).first()
    post = Posts.objects.filter(id=post_id).first()
    if not group:
        return Response({'error': 'Group does not exist'}, status=HTTP_404_NOT_FOUND)
    if not post:
        return Response({'error': 'Post does not exist'}, status=HTTP_404_NOT_FOUND)
    if post.author != user:
        return Response({'error': 'You are not the author of this post'}, status=HTTP_401_UNAUTHORIZED)
    if TimeOfJoining.objects.filter(user=user, group=group):
        return Response({'error': 'You do not belong to this group'}, status=HTTP_401_UNAUTHORIZED)
    PostGroupSharing.objects.create(group=group, post=post)
    return Response({'error': 'Post shared successfully'}, status=HTTP_200_OK)


@api_view(['POST'])
def share_to_user(request):
    user = request.user
    username = request.data.get('username')
    post_id = request.data.get('post_id')
    if not username or post_id:
        return Response({'error': 'Username or post id not provided'}, status=HTTP_400_BAD_REQUEST)
    shared_with = CustomUser.objects.filter(username=username).first()
    post = Posts.objects.filter(id=post_id).first()
    if not shared_with:
        return Response({'error': 'User does not exist'}, status=HTTP_404_NOT_FOUND)
    if not post:
        return Response({'error': 'Post does not exist'}, status=HTTP_404_NOT_FOUND)
    if post.author != user:
        return Response({'error': 'You are not the author of this post'}, status=HTTP_401_UNAUTHORIZED)
    PostUserSharing.objects.create(user=shared_with, post=post)
    return Response({'error': 'Post shared successfully'}, status=HTTP_200_OK)


@api_view(['GET'])
def get_group_posts(request):
    user = request.user
    group_id = request.data.get('group_id')
    if not group_id:
        return Response({'error': 'Group id is not provided'}, status=HTTP_400_BAD_REQUEST)
    group = Groups.objects.filter(id=group_id).first()
    if not group:
        return Response({'error': 'Group does not exist'}, status=HTTP_404_NOT_FOUND)
    user_group = TimeOfJoining.objects.filter(user=user, group=group).first()
    if not user_group:
        return Response({'error': 'You do not belong to this group'}, status=HTTP_401_UNAUTHORIZED)
    post_set = group.posts.order_by('timestamp').filter(timestamp__gte=user_group.timestamp)
    serialized_data = serializers.serialize('json', post_set)
    return HttpResponse(serialized_data, status=HTTP_200_OK)


@api_view(['GET'])
def get_user_posts(request):
    user = request.user
    group_set = user.group.all()
    post_set = []
    for group in group_set:
        post_set += list(group.group.posts.filter(timestamp__gte=group.timestamp))
    post_set.sort(key=lambda x:x.timestamp, reverse=True)
    serialized_data = serializers.serialize('json', post_set)
    return HttpResponse(serialized_data, status=HTTP_200_OK)


@api_view(['GET'])
def get_post(request):
    user = request.user
    post_id = request.data.get('post_id')
    if not post_id:
        return Response({'error': 'Post id is not provided'}, status=HTTP_400_BAD_REQUEST)
    post = Posts.objects.filter(id=post_id).first()
    if not post:
        return Response({'error': 'Post does not exist'}, status=HTTP_404_NOT_FOUND)
    groups = user.group.all().values('group')
    if not post.groups.filter(group__in=groups).first():
        return Response({'error': ''}, status=HTTP_401_UNAUTHORIZED)
    serialized_data = serializers.serialize('json', post)
    return HttpResponse(serialized_data, status=HTTP_200_OK)
