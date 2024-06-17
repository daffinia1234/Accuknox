from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from rest_framework import status
from . models import FriendRequest,Friends
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from .serializers import UserSerailizer, UserViewSerailizer,FriendRequestSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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
            if is_valid_email(search_keyword) :  # Assuming email search if there's an '@' character
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
    

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])   
def send_request(request,userID):
    from_user=request.user
    to_user=get_user(userID)
    if to_user is None:
        return Response({'User not Found'})
    friend_request, created=FriendRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
    if created:
        return Response('Friend request sent successfully',status=status.HTTP_200_OK)
    else:
        return Response('Request already sent')
    
def get_user(userID):
    try:
        return User.objects.get(id=userID)
    except User.DoesNotExist:
        return None
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_open_request(request):
    user=request.user
    open_requests=user.friend_request_received.all()
    serializer=FriendRequestSerializer(open_requests,many=True)
    return Response({'openrequests':serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept(request,requestID):

    user=request.user
    friend_request = FriendRequest.objects.filter(id=requestID).first()

    if friend_request is None:
        return Response('Not a valid friend request')
    elif user != friend_request.to_user:
        return Response('Not a valid friend request')
    else:   
        to_friends, created = Friends.objects.get_or_create(user=friend_request.to_user)
        from_friends, created = Friends.objects.get_or_create(user=friend_request.from_user)

        to_friends.friends_list.add(friend_request.from_user)
        from_friends.friends_list.add(friend_request.to_user)

        friend_request.delete()
        return Response('Friend request accepted',status=status.HTTP_200_OK)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reject(request,requestID):
    friend_request=FriendRequest.objects.filter(id=requestID).first()
    user=request.user
    if friend_request is None:
        return Response('Not a valid friend request')
    elif user!=friend_request.to_user:
        return Response('Not a valid friend request')
    else:
        friend_request.delete()
        return Response('Friend request Rejected')
        

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_friends_list(request):
    user=request.user
    friends= get_friends_of_user(user)
    friends_data = [{'id': friend.id, 'username': friend.username} for friend in friends]
    return Response({'friends' : friends_data})


def get_friends_of_user(user):
    friends_obj = get_object_or_404(Friends, user=user)
    friends = friends_obj.friends_list.all()
    return friends


