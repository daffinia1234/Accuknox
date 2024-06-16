from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class FriendRequest(models.Model):
    from_user=models.ForeignKey(User,related_name='friend_request_sent',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User,related_name='friend_request_received',on_delete=models.CASCADE)

class Friends(models.Model):
    user=models.ForeignKey(User,related_name='friendships',on_delete=models.CASCADE)
    friends_list=models.ManyToManyField(User, related_name='friends', blank=True)

