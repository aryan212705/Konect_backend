from datetime import datetime
from django.db import models
from users.models import CustomUser
from groups.models import Groups


class Posts(models.Model):
    title = models.CharField('Title', max_length=100)
    content = models.TextField(blank=True)
    author = models.ForeignKey(CustomUser, related_name='my_posts', on_delete=models.SET_NULL, null=True)
    postedOn = models.DateTimeField('Posted Time', default=datetime.now)
    editedOn = models.DateTimeField('Last Edited Time', auto_now=True)
    coverPic = models.ImageField(upload_to='coverpics', blank=True)


class PostGroupSharing(models.Model):
    group = models.ForeignKey(Groups, related_name='posts', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='groups', on_delete=models.CASCADE)
    timestamp = models.DateTimeField('Shared Time', default=datetime.now)


class PostUserSharing(models.Model):
    user = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='users', on_delete=models.CASCADE)
    timestamp = models.DateTimeField('Shared Time', default=datetime.now)
