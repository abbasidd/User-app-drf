from django.contrib import admin
from .models import User,UserProfile
admin.site.register(UserProfile)
admin.site.register(User)
# Register your models here.
