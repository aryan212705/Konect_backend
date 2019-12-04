from datetime import datetime
from users.models import CustomUser
from django.conf import settings
from django.db import models


class Groups(models.Model):
    id = models.BigIntegerField(primary_key = True)
    groupName = models.CharField('Group Name', max_length=50)
    creationDate = models.DateField('Group Creation Date', default=datetime.now)

    class Meta:
        verbose_name_plural = 'Groups'


class TimeOfJoining(models.Model):
    group = models.ForeignKey(Groups, related_name='user', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='group', on_delete=models.CASCADE)
    timestamp = models.DateTimeField('Joining Time', default=datetime.now)
    isAdmin = models.BooleanField('Admin', default=False)

    class Meta:
        verbose_name_plural = 'Time of Joining'
