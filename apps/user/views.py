from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser

from .models import CustomUser, Profile
from .serializers import (UserRegistrationSerializer, UserLoginSerializer,
                            UserSerializer, ProfileSerializer)
from .renderers import ProfileJSONRenderer


from apps.core.renderers import ApplicationJSONRenderer


class UserDetailUpdateView(generics.RetrieveUpdateAPIView):

    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def retrieve(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(request.user)

        return Response(serializer.data, status.HTTP_200_OK)

    def update(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)


class UserAuthenticationView(APIView):

    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        instance = CustomUser.objects.filter(**request.data)

        if instance.exists():
            serializer = UserLoginSerializer(instance.first())
            
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_201_CREATED)


class UserRegistrationView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={
                                                                        "request": request
                                                                    } )

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProfileViewFollowUnfollowView(generics.RetrieveAPIView, 
                                        generics.CreateAPIView, 
                                            generics.DestroyAPIView):
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer, ]

    def get_user_profile(self, request):
        return Profile.objects.get(user=request.user)

    def retrieve(self, request, username):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, username):
        instance = self.get_object()
        
        current_user_profile = self.get_user_profile(request)
        current_user_profile.following.add(instance)

        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, username):
        instance = self.get_object()
        
        current_user_profile = self.get_user_profile(request)
        current_user_profile.following.remove(instance)

        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)