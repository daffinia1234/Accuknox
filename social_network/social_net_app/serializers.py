from rest_framework import serializers
from django.contrib.auth.models import User
from . models import FriendRequest


class UserSerailizer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','password','email']

class UserViewSerailizer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','email']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=FriendRequest
        fields=['id','from_user','to_user']


