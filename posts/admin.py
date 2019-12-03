from django.contrib import admin
from .models import Posts, PostGroupSharing, PostUserSharing


admin.site.register(Posts)
admin.site.register(PostGroupSharing)
admin.site.register(PostUserSharing)
