from django.db import models
from django.contrib.auth.models import AbstractUser
import redis
from .celery import add_to_redis, push_posts
import pickle


r = redis.Redis(host='localhost', port=63, db=4)


class CustomUser(AbstractUser):
    followings = models.ManyToManyField(
        "CustomUser", related_name="followers", through="Followership", symmetrical=False)

    def follow(self, pk):
        user = CustomUser.objects.get(pk=pk)
        Followership.objects.get_or_create(
            from_user=self, to_user=user)
        r.delete(f"user-{self.id}")

    def unfollow(self, pk):
        user = CustomUser.objects.get(pk=pk)
        Followership.objects.filter(from_user=self, to_user=user).delete()
        r.delete(f"user-{self.id}")

    def get_follower_of_user(self):
        return self.followers.all()

    def get_following_of_user(self):
        return self.followings.all()

    def get_feed_of_user(self):
        posts = Post.objects.filter(
            author__in=self.followings.all()).order_by('-create_at')[:10]
        return posts


class Followership(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_person")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="from_person")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(CustomUser, models.CASCADE)
    body = models.CharField(max_length=144)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
