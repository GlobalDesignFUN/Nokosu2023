from rest_framework.decorators import api_view #, authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import InfoSerializer
from .models import Info, Profile

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint' : 'List of endpoint details'
        }
    ]
    return Response(routes)

# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
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

# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
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
