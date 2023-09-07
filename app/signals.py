# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from .models import UserModel


# @receiver(post_save, sender=UserModel)
# def create_user_profile(sender, instance, created, **kwargs):
#     print('ok')
#     if created:
#         user = User.objects.create_or_create(username=kwargs.get("username", None), password=kwargs.get("password", None))
#         instance.user = user
        

# @receiver(post_save, sender=UserModel)
# def save_user_profile(sender, instance, **kwargs):
#     print('ok')
#     instance.user = User.objects.create_or_create(username=kwargs.get("username", None), password=kwargs.get("password", None))
#     instance.save()