from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest


class UserSerailizer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','password','email']

class UserViewSerailizer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','email']


#Friend Request Serializer
class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField()
    to_user = serializers.StringRelatedField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'created_at', 'status']

class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['to_user']

