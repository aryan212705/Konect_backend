from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
import json

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
    group_set = user.group.all().order_by('-timestamp')
    groups = []
    for group in group_set:
        group_details = {
            'group_name': group.group.groupName,
            'time_of_joining': group.timestamp.strftime("%d %b, %H:%M"),
            'is_admin': group.isAdmin,
            'group_id': group.group.id,
            'admin': TimeOfJoining.objects.get(group=group.group, isAdmin=True).user.username
        }
        groups.append(group_details)
    serialized_data = json.dumps(groups)
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
        users = []
        for user in users_set:
            user_details = {
                'username': user.user.username,
                'time_of_joining': user.timestamp.strftime("%d %b, %H:%M"),
                'is_admin': user.isAdmin
            }
            users.append(user_details)
        serialized_data = json.dumps(users)
        return HttpResponse(serialized_data, status=HTTP_200_OK)
    else:
        return Response({'error': 'User do not belong to this group'}, status=HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_group_details(request):
    group_id = request.data.get('group_id')
    if not group_id:
        return Response({'error': 'group id is not present'}, status=HTTP_400_BAD_REQUEST)
    if not Groups.objects.filter(id=group_id):
        return Response({'error': 'Group not found'}, status=HTTP_404_NOT_FOUND)
    group = Groups.objects.filter(id=group_id).first()
    user_is_member = TimeOfJoining.objects.filter(user=request.user, group=group).first()
    if not user_is_member:
        return Response({'error': 'User do not belong to this group'}, status=HTTP_401_UNAUTHORIZED)
    else:
        group_details = {
            'group_id': group.id,
            'group_name': group.groupName,
            'date_of_creation': group.creationDate.strftime("%d %b"),
            'time_of_joining': user_is_member.timestamp.strftime("%d %b, %H:%M")
        }
        serialized_data = json.dumps(group_details)
        return HttpResponse(serialized_data, status=HTTP_200_OK)
