from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    followings = models.ManyToManyField("CustomUser")

    def follow(self, user):
        # u = CustomUser.objects.get(id=pk)
        self.followings.add(user)

    def unfollow(self, user):
        self.followings.remove(user)

    def get_following_of_user(self):
        return self.followings.all()

    def get_feed_of_user(self):
        # followings = self.get_following_of_user()
        posts = Post.objects.filter(author__in=self.followings.all()).prefetch_related("author").order_by(
            '-create_at')
        return posts


class Post(models.Model):
    author = models.ForeignKey(CustomUser, models.CASCADE)
    body = models.CharField(max_length=144)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
