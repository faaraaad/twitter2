from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from redis import Redis
from django.contrib.auth import get_user_model


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
