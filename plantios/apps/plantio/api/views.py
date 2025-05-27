from rest_framework import viewsets
from plantios.apps.plantio.models import Plantio
from apps.plantio.api.serializers import PlantioSerializer

class PlantioViewSet(viewsets.ModelViewSet):
    queryset = Plantio.objects.all()
    serializer_class = PlantioSerializer
    http_method_names = ["get", "post", "put", "delete"]


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from plantios.apps.plantio.models import Plantio
# from apps.plantio.api.serializers import PlantioSerializer

# class PlantioListCreateAPIview(APIView):
#     def get(self, request):
#         plantios = Plantio.objects.all()
#         serializer = PlantioSerializer(plantios, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PlantioSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PlantioDetailAPIview(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Plantio, pk=pk)

#     def get(self, request, pk):
#         plantio = self.get_object(pk)
#         serializer = PlantioSerializer(plantio)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         plantio = self.get_object(pk)
#         serializer = PlantioSerializer(plantio, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         produto = self.get_object(pk)
#         produto.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)