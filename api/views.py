from django.shortcuts import render
from .models import CustomUSer, AgentUser, HouseModel
from .serializers import RegisterUserSerializer, HouseSerializer, AgentProfileSerializer,AgentKYCSerializer
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


class AgentProfileVerificationView(APIView):
    permission_classes = [IsAuthenticated, IsAgent]

    def put(self, request ):
        user = request.user
        try:
         agent = AgentUser.objects.get(user= user)
        except AgentUser.DoesNotExist:
            return Response({"message" : "Agent Does Not Exist " },  status=status.HTTP_404_NOT_FOUND  )  
        
        serializer = AgentProfileSerializer(agent, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save(verification_step = 2)
            return Response({
                "success" : True,
                "message" : "Profile Updated Succesfully",
                "data" : serializer.data,
                "errors" : serializer.errors,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success" : False,
                "message" : "Unable to Update Profile",
                "data" : serializer.data,
                "errors" : serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

class AgentKYCView(APIView):
    permission_classes = [IsAuthenticated, IsAgent]
    def put(self, request):
        user =  request.user
        try:
            agent = AgentUser.objects.get(user=user)
        except AgentUser.DoesNotExist:
            return Response({"message": "Agent Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AgentKYCSerializer(agent, data = request.data)

        if serializer.is_valid():
            serializer.save(verification_step="3", verification_status="Success" )
            return Response({ 
                "success" : True,  
                "message" : "KYC Verification Succesfull",  
                "data" : serializer.data,  
                "errors" : serializer.errors
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success" : False,
                "message" : "Unable to Verify KYC",
                "data" : serializer.data,
                "errors" : serializer.errors,
            },status=status.HTTP_400_BAD_REQUEST )

class HouseView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
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
            return Response(
                { 
                    "success" : True,  
                    "message" : "House Uploaded Succesfully",  
                    "data" : serializer.data,  
                    "error" : serializer.errors,  
                 
                 }, status=status.HTTP_201_CREATED)
        else:
            return Response( {
                "success" : False,
                "message" : "House Upload Failed",
                "data" : serializer.data,
                "errors" : serializer.errors,

            }, status=status.HTTP_400_BAD_REQUEST)


    
    