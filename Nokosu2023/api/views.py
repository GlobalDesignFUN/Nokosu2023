from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint' : 'List of endpoint details'
        }
    ]
    return Response(routes)
