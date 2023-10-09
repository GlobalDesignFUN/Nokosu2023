from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import InfoSerializer, UserSerializer, ProfileSerializer
from .models import Info, Profile, User

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint' : 'List of endpoint details'
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
        return Response(serializer.errors)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile(request, pk):
    try:
        profile = Profile.objects.get(user=pk)
    except:
        return Response({'Error':'Invalid Id'})
    
    if not (request.user.is_staff or profile.id==pk):
        return Response({'detail': 'You do not have permission to perform this action.'})
    
    if request.method == 'GET':
        profileSerializer_data = ProfileSerializer(profile, many=False).data
        profileSerializer_data['user'] = UserSerializer(profile.user, many=False).data
        return Response(profileSerializer_data)
    
    if request.method == 'PUT':
        return Response('PUT')
    if request.method == 'DELETE':
        profile.delete()
        return Response({'detail': 'Deleted successful'})
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def profileList():
    profiles = Profile.objects.all()
    profSerializer = ProfileSerializer(profiles, many=True)
    profile_list = []
    for profile in profSerializer.data:
        user = User.objects.get(id=profile['user'])
        profile['user'] = UserSerializer(user, many=False).data
        profile_list.append(profile)
    return Response(profile_list)

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
            return Response({'error': 'Invalid credentials'})
        
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
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def InfoItem(request, pk):
    try:
        info = Info.objects.get(id=pk)
    except:
        return Response({'Error':'Invalid Id'})
    if request.method == 'GET':
        serializer = InfoSerializer(info, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = InfoSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        info.delete()
        return Response({'detail': 'Deleted the info with id:{}'.format(pk)})