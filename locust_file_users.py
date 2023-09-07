from locust import HttpUser, task, between, TaskSet
from gevent.pool import Group
import pickle
import random
from faker import Faker

num_of_parallel_requests = 30

with open("token.dump", "rb") as f:
    tokens = pickle.load(f)

fake = Faker()


class User(HttpUser):
    wait_time = between(0.05, 0.1)

    @task(10)
    def test_api(self):
        url = '/app/posts'

        group = Group()
        for i in range(0, num_of_parallel_requests):
            user = random.choice(tokens)
            headers = {"Authorization": "Bearer " + user}
            group.spawn(lambda: self.client.get(url, headers=headers))
        group.join()

    @task(1)
    def create_post(self):
        url = '/app/posts/'

        group = Group()
        for i in range(0, num_of_parallel_requests):
            user = random.choice(tokens)
            data = {
                "body": fake.sentence()
            }
            headers = {"Authorization": "Bearer " + user}
            group.spawn(lambda: self.client.post(url, json=data, headers=headers))
        group.join()

    # @task(10)
    # def test_public(self):
    #     url = '/app/public'
    #
    #     group = Group()
    #     for i in range(0, num_of_parallel_requests):
    #         group.spawn(lambda: self.client.get(url))
    #     group.join()
