from rest_framework.decorators import api_view
import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from .serializers import UserSerailizer, UserViewSerailizer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle
from django.core.cache import cache
from .models import FriendRequest
from .serializers import FriendRequestSerializer, FriendRequestCreateSerializer
from django.utils import timezone
from datetime import timedelta

# Create your views here.



@api_view(['POST'])
def Login(request):
    try:
        user=get_object_or_404(User,username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail":"Invalid Credential"},status=status.HTTP_404_NOT_FOUND)
        token,created=Token.objects.get_or_create(user=user)
        serializer=UserViewSerailizer(instance=user)
        return Response({"token":token.key,"user":serializer.data})
    
    except:
        return Response({"detail":"user not found"},status=status.HTTP_404_NOT_FOUND)
 

@api_view(['POST'])
def Signup(request):
    serializer=UserSerailizer(data=request.data)
    
    if serializer.is_valid():
        user=serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        serializer = UserViewSerailizer(instance=user)
        token=Token.objects.create(user=user)
        return Response({"token":token.key,"user":serializer.data},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'detail':'Logged out successfully'},status=status.HTTP_200_OK)
    except:
        return Response({'detail':'logout failed'},status=status.HTTP_400_BAD_REQUEST)




# search API
class UserSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    serializer_class = UserViewSerailizer
    pagination_class = UserSearchPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        queryset = User.objects.order_by('username')
        search_keyword = self.request.query_params.get('search', None)
        
        if search_keyword:
            if '@' in search_keyword:  # Assuming email search if there's an '@' character
                queryset = queryset.filter(email__iexact=search_keyword)
            else:
                queryset = queryset.filter(username__icontains=search_keyword) 
                           
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

