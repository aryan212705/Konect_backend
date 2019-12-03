from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.utils import json

from groups.models import Groups, TimeOfJoining
from users.models import CustomUser

@api_view(['POST'])
def create_group(request):
    group_name = request.data.get('group_name')
    if not group_name:
        return Response({'error': 'Please provide a group name'}, status=HTTP_400_BAD_REQUEST)
    group = Groups.objects.create(groupName=group_name)
    TimeOfJoining.objects.create(group=group, user=request.user, isAdmin=True)
    return Response({'message': 'Group created successfully'}, status=HTTP_200_OK)


@api_view(['POST'])
def add_member(request):
    username = request.data.get('username')
    group_id = request.data.get('group_id')
    if not group_id or not username:
        return Response({'error': 'username or group id is not present'}, status=HTTP_400_BAD_REQUEST)
    if not Groups.objects.filter(id=group_id):
        return Response({'error': 'Group not found'}, status=HTTP_404_NOT_FOUND)
    if not CustomUser.objects.filter(username=username):
        return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)
    user = CustomUser.objects.filter(username=username).first()
    group = Groups.objects.filter(id=group_id).first()
    if TimeOfJoining.objects.filter(user=user, group=group):
        return Response({'error': 'User already in group'}, status=HTTP_409_CONFLICT)
    TimeOfJoining.objects.create(user=user, group=group)
    return Response({'message': 'User successfully added to group'}, status=HTTP_200_OK)


@api_view(['GET'])
def user_groups(request):
    user = request.user
    group_set = user.group.all()
    serialized_data = serializers.serialize('json', group_set)
    return HttpResponse(serialized_data, status=HTTP_200_OK)


@api_view(['GET'])
def group_members(request):
    group_id = request.data.get('group_id')
    if not group_id:
        return Response({'error': 'group id is not present'}, status=HTTP_400_BAD_REQUEST)
    if not Groups.objects.filter(id=group_id):
        return Response({'error': 'Group not found'}, status=HTTP_404_NOT_FOUND)
    group = Groups.objects.filter(id=group_id).first()
    if TimeOfJoining.objects.filter(user=request.user, group=group):
        users_set = group.user.all()
        serialized_data = serializers.serialize('json', users_set)
        return HttpResponse(serialized_data, status=HTTP_200_OK)
    else:
        return Response({'error': 'User do not belong to this group'}, status=HTTP_401_UNAUTHORIZED)