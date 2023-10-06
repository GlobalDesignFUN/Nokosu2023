from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InfoSerializer
from .models import Info

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
