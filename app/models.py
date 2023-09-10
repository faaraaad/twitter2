from django.db import models
from django.contrib.auth.models import AbstractUser
import redis


r = redis.Redis(host='localhost', port=63, decode_responses=True, db=10)


class CustomUser(AbstractUser):
    followings = models.ManyToManyField(
        "CustomUser", related_name="followers", through="Followership", symmetrical=False)

    def follow(self, user):
        relationship, created = Followership.objects.get_or_create(
            from_user=self, to_user=user)
        r.delete(f"user-{self.id}")

    def unfollow(self, user):
        Followership.objects.filter(from_user=self, to_user=user).delete()
        r.delete(f"user-{self.id}")

    def get_follower_of_user(self):
        return self.followers.all()

    def get_following_of_user(self):
        return self.followings.all()

    def get_feed_of_user(self):
        if feed := r.lrange(f"user-{self.id}", 0, -1):
            id_of_posts = [int(i) for i in feed]
            posts = Post.objects.filter(id__in=id_of_posts)
            return posts
        else:
            posts = Post.objects.filter(
                author__in=self.followings.all()).order_by('-create_at')
            if posts:
                r.lpush(f"user-{self.id}", *[post.id for post in posts])
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
        followers = CustomUser.objects.get(id=self.author.id).followers.all()
        for user in followers:
            r.lpush(f"user-{user.id}", self.id)

    def __str__(self):
        return self.body
