from django.db import models
from django.contrib.auth.models import AbstractUser


class Post2018To2022(models.Model):
    class Meta:
        managed = False
        # db_table = 'app_postmodel_default'
        db_table = 'app_post_2018_to_2022'

    author = models.ForeignKey("CustomUser", models.CASCADE)
    body = models.CharField(max_length=144)
    create_at = models.DateTimeField(auto_now_add=True)


class Post2023To2024(models.Model):
    class Meta:
        managed = False
        # db_table= "app_postmodel_post_partitioned_create_from_2022_to_2023"
        db_table = 'app_post_2022_to_2024'

    author = models.ForeignKey("CustomUser", models.CASCADE)
    body = models.CharField(max_length=144)
    create_at = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    followings = models.ManyToManyField(
        "CustomUser", related_name="followers", through="Followership", symmetrical=False)

    def follow(self, pk):
        user = CustomUser.objects.get(pk=pk)
        Followership.objects.get_or_create(
            from_user=self, to_user=user)

    def unfollow(self, pk):
        user = CustomUser.objects.get(pk=pk)
        Followership.objects.filter(from_user=self, to_user=user).delete()

    def get_follower_of_user(self):
        return self.followers.all()

    def get_following_of_user(self):
        return self.followings.all()

    def get_feed_of_user(self):
        recent_posts = Post2018To2022.objects.filter(
            author__in=self.followings.all().only("id")).order_by('-create_at')

        old_posts = Post2023To2024.objects.filter(
            author__in=self.followings.all().only("id")).order_by('-create_at')

        combined_posts = recent_posts.union(old_posts).order_by("filter")
        return combined_posts


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


from django.db import models
from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel


class PostModel(PostgresPartitionedModel):
    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["create_at"]

    author = models.ForeignKey(CustomUser, models.CASCADE)
    body = models.CharField(max_length=144)
    create_at = models.DateTimeField(auto_now_add=True)
