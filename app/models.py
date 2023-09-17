from django.db import models
from django.contrib.auth.models import AbstractUser
import redis
from .celery import add_to_redis, push_posts
import pickle


r = redis.Redis(host='localhost', port=63, db=4, decode_responses=True)


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

    def get_recent_feed_of_user(self, cache_size):
        if feed := r.lrange(f"user-{self.id}", 0, cache_size):
            return Post.objects.filter(id__in=feed)
        else:
            posts = Post.objects.filter(
                author__in=self.followings.all().only("id")).order_by('-create_at')[:cache_size]
            if posts:
                posts_id = [post.id for post in posts]
                print(posts_id)
                r.lpush(f"user-{self.id}", *posts_id)
        return posts

    def get_feed_of_user(self, cache_size):
        posts = Post.objects.filter(
            author__in=self.followings.all().only("id")).order_by('-create_at')[:cache_size]
        return posts


class Followership(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_person")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="from_person")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(CustomUser, models.CASCADE)
    body = models.CharField(max_length=144)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        add_to_redis(self.author.id, self.id)

    def __str__(self):
        return self.body
