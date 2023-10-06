from rest_framework.decorators import api_view
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

@api_view(['GET', 'POST'])
def InfoList(request):
    print(request.user.id)
    currentUser=Profile.objects.get(user=request.user.id)
    print(currentUser.user.username)
    if request.method == 'GET':
        infos = Info.objects.all()
        serializer = InfoSerializer(infos, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = request.data
        info = Info.objects.create(
            topic=data['topic'],
            description=data['description'],
            photo=data['photo'],
            location=data['location'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            address=data['address'],
            group=data['group'],
            createdBy=currentUser,
            emotion=data['emotion'],
            cultural=data['cultural'],
            physical=data['physical'],
        )
        serializer = InfoSerializer(info, many=False)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def InfoItem(request, pk):
    info = Info.objects.get(id=pk)
    if request.method == 'GET':
        serializer = InfoSerializer(info, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = InfoSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        info.delete()
        return Response('Deleted')
