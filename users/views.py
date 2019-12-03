from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import *

from users.models import CustomUser


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Please provide username and password both'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
    else:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    return Response({'token': token.key}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    name = request.data.get('name')
    if not username or not password:
        return Response({'error': 'Please provide username and password both'}, status=HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(username=username):
        return Response({'error': 'Username already taken. Please provide something unique'}, status=HTTP_409_CONFLICT)
    try:
        user = CustomUser.objects.create_user(username=username, password=password, first_name=name or '')
    except:
        return Response({'error': 'Something went wrong'}, status=HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)
