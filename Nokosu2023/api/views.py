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

@api_view(['GET'])
def getInfos(request):
    infos = Info.objects.all()
    serializer = InfoSerializer(infos, many=True)
    return Response(serializer.data)