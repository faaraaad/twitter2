from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from redis import Redis
from django.contrib.auth import get_user_model
import pickle


r = Redis(host="localhost", port=63, db=4)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter.settings')

app = Celery('app')
app.conf.enable_utc = False
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def add_to_redis(self, author_id, post):
    print("received to celery")
    customuser = get_user_model()
    followers = customuser.objects.get(id=author_id).followers.all()
    for user in followers:
        r.lpush(f"user-{user.id}", post)
        r.ltrim(f"user-{user.id}", 10, -1)


@app.task(bind=True)
def push_posts(self, posts, user_id):
    posts_pickle = [pickle.dumps(post) for post in posts]
    r.lpush(f"user-{user_id}", *posts_pickle)
    r.ltrim(f"user-{user_id}", 10, -1)
