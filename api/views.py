from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import InfoSerializer, UserSerializer, ProfileSerializer
from .models import Info, Profile

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
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            try:
                profSerializer = ProfileSerializer(data={'user':user.id, 'photo': request.data['photo']})
            except:
                profSerializer = ProfileSerializer(data={'user':user.id, 'photo': ''})
            if profSerializer.is_valid():
                profSerializer.save()
            else:
                Profile.objects.create(user=user)
            return Response({'token': token.key, 'ProfileErrors': profSerializer.errors})
        return Response(serializer.errors)

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
        return Response('Deleted')
