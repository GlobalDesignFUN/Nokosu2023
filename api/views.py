from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.conf import settings
from django_rest_passwordreset.models import ResetPasswordToken
from pathlib import Path
from .serializers import InfoSerializer, UserSerializer, ProfileSerializer, GroupSerializer
from .models import Info, Profile, User, Group, Default_Profile_Image
from .forms import PasswordForm, RegistrationAPI
import json
import pyrebase
import os 

firebase = pyrebase.initialize_app(settings.FIREBASECONFIG)
storage = firebase.storage()

def redirectbase(_):
    return redirect(getRoutes)

@api_view(['GET'])
def getRoutes(_):
    routes = [
        {
            'Welcome!' : 'NOKOSU Backend',
            'Developed By' : 'Global Design 2023 Team'
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
                    'Group':[
                        {
                            'Description' : 'Get a List of all Group objects',
                            'Method' : 'GET',
                            'URL' : '/api/groups/',
                        },
                        {
                            'Description' : 'Create a Group object',
                            'Method' : 'POST',
                            'URL' : '/api/groups/',
                        },
                        {
                            'Description' : 'Get all Info objects in a Group with given id',
                            'Method' : 'GET',
                            'URL' : '/api/groups/0',
                        },
                        {
                            'Description' : 'Update a Group object with given id',
                            'Method' : 'PUT',
                            'URL' : '/api/groups/0',
                        },
                        {
                            'Description' : 'Delete a Group object with given id',
                            'Method' : 'DELETE',
                            'URL' : '/api/groups/0',
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
                {
                    'email':[
                        {
                            'Description' : 'Getting a password reset email with the token',
                            'Method' : 'POST',
                            'URL' : '/api/password_reset/',
                        },
                        {
                            'Description' : 'Updating the password with token',
                            'Method' : 'POST',
                            'URL' : '/api/password_reset/confirm/',
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
                    'Password reset form': '/password/token'
                },
            ]
        }
    ]
    return Response(routes)

def passwordReset(request, token):
    if request.method == 'POST':
        try:
            form = PasswordForm(request.POST)

            try:
                reset_token = ResetPasswordToken.objects.get(key=token)
            except ResetPasswordToken.DoesNotExist:
                return render(request, 'api/password_reset_response.html', {'status':404})

            if form.is_valid():
                reset_token.user.set_password(form.cleaned_data['password1'])
                reset_token.user.save()
                reset_token.delete()
                return render(request, 'api/password_reset_response.html', {'status':200})
            return render(request, 'api/password_reset_form.html', {'form': form})
        
        except Exception as e:
            return render(request, 'api/password_reset_response.html', {'error':e})
        
    if request.method == 'GET':
        form = PasswordForm(initial={'token': token})
        return render(request, 'api/password_reset_form.html', {'form': form})

        # #test print
        # print('==============================PASSWORD RESET START==============================')
        # form = PasswordForm(request.POST)
        # reset_password_url = "{}://{}/api/password_reset/confirm/".format(request.scheme, request.get_host())
        # data = {"password": request.POST.get('password'), "token": token}
        # #test print
        # print(data['password'])
        # print(data['token'])
        # print(reset_password_url)
        # try:
        #     response = requests.post(reset_password_url, json=data)
        #     #test print
        #     print("Response code : "+str(response.status_code))
        #     if response.status_code == 200:
        #         #test print
        #         print('==============================PASSWORD RESET END 200==============================')
        #         return render(request, 'api/password_reset_response.html', {'status':200})
                
        #     if response.status_code == 400:
        #         form.errors['password'] = response.json()['password']
        #         #test print
        #         print('==============================PASSWORD RESET END 400==============================')
        #         return render(request, 'api/password_reset_form.html', {'form': form})
        #     if response.status_code == 404:
        #         #test print
        #         print('==============================PASSWORD RESET END 404==============================')
        #         return render(request, 'api/password_reset_response.html', {'status':404})
            
        #     #test print
        #     print('==============================PASSWORD RESET END UNIDTFD==============================')
        #     return render(request, 'api/password_reset_response.html', {'error': 'Something went wrong. Please try again.'})
        # except Exception as e:
        #     #test print
        #     print('==============================PASSWORD RESET ERR=============================='+e)
        #     return render(request, 'api/password_reset_response.html', {'error':e})

@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        regForm = RegistrationAPI(request.POST)
        if regForm.is_valid():
            serializer.initial_data._mutable = True
            serializer.initial_data['password'] = regForm.cleaned_data['password1']
            if serializer.is_valid():
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                profileSerializer = ProfileSerializer(data={'user':user.id, 'photo': request.data.get('photo'), 'url':''})
                if profileSerializer.is_valid():
                    prof = profileSerializer.save()
                    storage.child("ProfilePics/" + str(prof.id)).put(profileSerializer.validated_data['photo'])
                    url = storage.child("ProfilePics/" + str(prof.id)).get_url(None)
                    prof.url = url
                    prof.save()
                else:
                    Profile.objects.create(user=user)
                profileSerializer_data = ProfileSerializer(Profile.objects.get(user=user.id), many=False).data
                profileSerializer_data['user'] = UserSerializer(user, many=False).data
                profileSerializer_data['errors'] = profileSerializer.errors
                return Response({'token': token.key, 'profile':profileSerializer_data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(json.loads(regForm.errors.as_json()), status=status.HTTP_400_BAD_REQUEST)
    
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
    
    if not (request.user.is_staff or (Profile.objects.get(user=request.user)==profile)):
        return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'PUT':
        userSerializer = UserSerializer(profile.user, data=request.data, partial=True)
        userSerializer.initial_data._mutable = True
        userSerializer.initial_data['password'] = 'temp' # Ignored by the update() of serializer
        profileSerializer = ProfileSerializer(profile, data={'photo': request.data.get('photo'), 'url':''})
        isProfileValid = profileSerializer.is_valid()
        if userSerializer.is_valid():
            userSerializer.save()
            if isProfileValid:
                storage.child("ProfilePics/" + str(profile.id)).put(profileSerializer.validated_data['photo'])
                url = storage.child("ProfilePics/" + str(profile.id)).get_url(None)
                profileSerializer.validated_data['url'] = url
                profileSerializer.save()
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
            storage.delete("ProfilePics/" + str(profile.id), 'tkn')
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
def infoList(request):
    if request.method == 'GET':
        infos = Info.objects.all()
        serializer = InfoSerializer(infos, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = InfoSerializer(data=request.data)
        serializer.initial_data._mutable = True
        serializer.initial_data['createdBy'] = Profile.objects.get(user=request.user.id).id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def infoItem(request, pk):
    try:
        info = Info.objects.get(id=pk)
    except:
        return Response({'error':'Invalid Info Id'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = InfoSerializer(info, many=False)
        return Response(serializer.data)
    
    if not (request.user.is_staff or (Profile.objects.get(user=request.user)==info.createdBy)):
        return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'PUT':
        serializer = InfoSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        info.photo.delete()
        info.delete()
        return Response({'detail': 'Deleted the info with id:{}'.format(pk)})
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def groupList(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        serializer.initial_data._mutable = True
        serializer.initial_data['createdBy'] = Profile.objects.get(user=request.user.id).id
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def groupItem(request, pk):
    try:
        group = Group.objects.get(id=pk)
    except:
        return Response({'error':'Invalid Group Id'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        infos = Info.objects.filter(group=group)
        serializer = InfoSerializer(infos, many=True)
        return Response(serializer.data)
    
    if not (request.user.is_staff or (Profile.objects.get(user=request.user)==group.createdBy)):
        return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        group.delete()
        return Response({'detail': 'Deleted the group with id:{}'.format(pk)})
   