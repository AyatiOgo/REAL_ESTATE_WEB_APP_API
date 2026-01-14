from django.shortcuts import render
from .models import CustomUSer, AgentUser, HouseModel
from .serializers import RegisterUserSerializer, HouseSerializer, AgentProfileSerializer,AgentKYCSerializer, UserProfileSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .permissons import IsAgent
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .paginators import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend

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
        serializer = AgentKYCSerializer(agent, data=request.data)

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
        
class AgentProfileView(APIView):
    def get(self, request, user):
        try:
            agent = AgentUser.objects.get(user__username = user)
        except AgentUser.DoesNotExist:
            return Response({"message": "Agent Doesn't exist"})
        
        serializer = AgentProfileSerializer(agent)
        return Response({
            "success" : True,
            "message": "Agent Profile Feched",
            "data" : serializer.data
        })

class HouseView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated(), IsAgent()]
    paginator_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['house_category']

    def get(self, request):
        queryset =  HouseModel.objects.all()
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self )

        paginator = self.paginator_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer  = HouseSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
    
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

class UserProfileView(APIView):
    def get(self, request, user):
        try:
            user_profile = CustomUSer.objects.get(username = user)
        except CustomUSer.DoesNotExist:
            return Response({"message": "user does not exist"})
        
        serializer = UserProfileSerializer(user_profile)
        return Response({
            "success": True,
            "message": "user profile fetched",
            "data": serializer.data,
        })