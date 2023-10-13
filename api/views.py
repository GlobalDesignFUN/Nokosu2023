from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from .serializers import InfoSerializer, UserSerializer, ProfileSerializer
from .models import Info, Profile, User, Default_Profile_Image

def redirectbase(_):
    return redirect(getRoutes)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Global Design 2023' : 'Welcome to NOKOSU backend'
        },
        {
            'API Endpoints' : [
                {
                    'Info':[
                        {
                            'Description' : 'Get a List of all Info objects',
                            'Method' : 'GET',
                            'URL' : '/api/infos/',
                        },
                        {
                            'Description' : 'Create an Info object',
                            'Method' : 'POST',
                            'URL' : '/api/infos/',
                        },
                        {
                            'Description' : 'Get a single Info object with given id',
                            'Method' : 'GET',
                            'URL' : '/api/infos/0',
                        },
                        {
                            'Description' : 'Update an Info object with given id',
                            'Method' : 'PUT',
                            'URL' : '/api/infos/0',
                        },
                        {
                            'Description' : 'Delete an Info object with given id',
                            'Method' : 'DELETE',
                            'URL' : '/api/infos/0',
                        },
                    ]
                },
                {
                    'Profile':[
                        {
                            'Description' : 'Get a List of all User Profile objects',
                            'Method' : 'GET',
                            'URL' : '/api/profiles/',
                        },
                        {
                            'Description' : 'Get a single User Profile object with given id',
                            'Method' : 'GET',
                            'URL' : '/api/profiles/0',
                        },
                        {
                            'Description' : 'Update a User Profile object with given id',
                            'Method' : 'PUT',
                            'URL' : '/api/profiles/0',
                        },
                        {
                            'Description' : 'Delete a User object with given id',
                            'Method' : 'DELETE',
                            'URL' : '/api/profiles/0',
                        },
                    ]
                },
                {
                    'User':[
                        {
                            'Description' : 'Create a User Profile and return access token',
                            'Method' : 'POST',
                            'URL' : '/api/users/register/',
                        },
                        {
                            'Description' : 'Return access token',
                            'Method' : 'POST',
                            'URL' : '/api/users/login',
                        },
                        {
                            'Description' : 'Delete access token',
                            'Method' : 'POST',
                            'URL' : '/api/users/logout',
                        },
                    ]
                },
            ]
        },
        {
            'Web Templates' : [
                {
                    'Admin Site': '/admin/'
                },
                {
                    'Password reset view': 'Under construction'
                },
            ]
        }
    ]
    return Response(routes)

@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password1 = serializer.validated_data.get('password')
            password2 = request.data.get('password2')
            if password1 != password2:
                return Response({'password2': 'Passwords do not match'})
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            profileSerializer = ProfileSerializer(data={'user':user.id, 'photo': request.data.get('photo')})
            if profileSerializer.is_valid():
                profileSerializer.save()
            else:
                Profile.objects.create(user=user)
            profileSerializer_data = ProfileSerializer(Profile.objects.get(user=user.id), many=False).data
            profileSerializer_data['user'] = UserSerializer(user, many=False).data
            profileSerializer_data['errors'] = profileSerializer.errors
            return Response({'token': token.key, 'profile':profileSerializer_data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def profileList(_):
    profiles = Profile.objects.all()
    profSerializer = ProfileSerializer(profiles, many=True)
    profile_list = []
    for profile in profSerializer.data:
        if profile['user']:
            profile['user'] = UserSerializer(User.objects.get(id=profile['user']), many=False).data
        profile_list.append(profile)
    return Response(profile_list)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except:
        return Response({'error':'Invalid Profile Id'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        profileSerializer_data = ProfileSerializer(profile, many=False).data
        if profile.user:
            profileSerializer_data['user'] = UserSerializer(profile.user, many=False).data
        return Response(profileSerializer_data)
    
    if not (request.user.is_staff or profile.id==pk):
        return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'PUT':
        userSerializer = UserSerializer(profile.user, data=request.data)
        profileSerializer = ProfileSerializer(profile, data={'photo': request.data.get('photo')})
        isProfileValid = profileSerializer.is_valid()
        if userSerializer.is_valid():
            userSerializer.save()
            if isProfileValid:
                profile.photo.delete()
                profile.photo = profileSerializer.validated_data.get('photo')
                profile.save()
            profileSerializer_data = ProfileSerializer(profile, many=False).data
            profileSerializer_data['user'] = UserSerializer(profile.user, many=False).data
            profileSerializer_data['errors'] = profileSerializer.errors
            return Response(profileSerializer_data)
        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        if profile.user:
            profile.user.delete()
        if profile.photo != Default_Profile_Image:
            profile.photo.delete()
            profile.photo = Default_Profile_Image
            profile.save()
        return Response({'detail': 'Deleted successful'})

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            profileSerializer_data = ProfileSerializer(Profile.objects.get(user=user.id), many=False).data
            profileSerializer_data['user'] = UserSerializer(user, many=False).data
            return Response({'token': token.key, 'profile':profileSerializer_data})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        request.auth.delete()
        return Response({'detail': 'Logout successful'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def InfoList(request):
    if request.method == 'GET':
        infos = Info.objects.all()
        serializer = InfoSerializer(infos, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = InfoSerializer(data=request.data)
        serializer.initial_data['createdBy'] = Profile.objects.get(user=request.user.id).id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def InfoItem(request, pk):
    try:
        info = Info.objects.get(id=pk)
    except:
        return Response({'error':'Invalid Info Id'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = InfoSerializer(info, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = InfoSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        info.photo.delete()
        info.delete()
        return Response({'detail': 'Deleted the info with id:{}'.format(pk)})