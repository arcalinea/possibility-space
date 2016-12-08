from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib import auth

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    num_invited = models.IntegerField(default=0)
    def __str__(self):
        return self.user_text

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.exchange_text

class Exchange(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    request_date = models.DateTimeField('date requested')
    deliver_date = models.DateTimeField('date delivered')
    giver = models.ForeignKey(Profile, related_name='giver')
    receiver = models.ForeignKey(Profile, related_name='receiver')
    category = models.ForeignKey(Category, related_name='category')
    def __str__(self):
        return self.exchange_text


exchanges = Exchange.objects.all()
# for exch in exchanges:
#     print "Exchange name", exch.name
#     print "Exchange description", exch.description
