from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializer import *


@api_view(['GET'])
def getAllBikes(request):

    bike = Bike.objects.all()
    serializer = BikeSerializer(bike, many=True)
    return Response(serializer.data)
