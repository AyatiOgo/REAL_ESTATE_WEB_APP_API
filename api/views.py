from django.shortcuts import render
from .models import CustomUSer, AgentUser, HouseModel
from .serializers import RegisterUserSerializer, HouseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissons import IsAgent
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
class HouseView(APIView):

    def get_permissions(self, request):
        if request.method == 'GET':
            return []
        return [IsAuthenticated(), IsAgent()]

    def get(self, request):
        house =  HouseModel.objects.all()
        serializer  = HouseSerializer(house, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        agent = request.user
        serializer = HouseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(house_agent = agent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


    
    