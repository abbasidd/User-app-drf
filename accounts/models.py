from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    block_user = models.ManyToManyField('self', blank=True)
    last_online = models.DateTimeField(blank=True, null=True)
    groups = models.ManyToManyField(Group,related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission,related_name='user_permission')

    @staticmethod
    def update_user_activity(user):
        print(timezone.now())
        """Updates the timestamp a user has for their last action. Uses UTC time."""
        User.objects.update_or_create(
            id=user.id, defaults={'last_online': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=timedelta(minutes=15)):
        """
        Gathers OnlineUserActivity objects from the database representing active users.
        :param time_delta: The amount of time in the past to classify a user as "active". Default is 15 minutes.
        :return: QuerySet of active users within the time_delta
        """
        starting_time = timezone.now() - time_delta
        return User.objects.filter(last_activity__gte=starting_time).order_by('-last_online')

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='userProfile')
    email_confirmation = models.BooleanField(default=False)
    birth_date = models.DateField()
    bio = models.TextField()
    picture = models.ImageField(
        upload_to='dp', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.user.username
