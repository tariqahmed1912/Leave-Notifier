from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_details")
    role = models.CharField(max_length=40, blank=True)
    dept = models.CharField(max_length=40, blank=True)
    #profile_pic = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_user_details(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_user_details(sender, instance, **kwargs):
    instance.user_details.save()

class FacultyDetails(models.Model):
    user = models.CharField(max_length=50)
    dept = models.CharField(max_length=40)
    date_of_leave = models.DateField()
    no_of_days = models.IntegerField()
    reason = models.TextField()
    permission = models.IntegerField(null=True, blank=True, default=-1)
    
    def __str__(self):
        return self.user