from django.contrib.auth.models import User
from .models import profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=User)
def creat_profile(sender,instance,created,**kwargs):
    if created:
        profile.objects.create(staff=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()
