from django.http import JsonResponse

def getRoutes(request):
    routes = [
        {
            'Endpoint' : 'List of endpoint details'
        }
    ]
    return JsonResponse(routes, safe=False)
