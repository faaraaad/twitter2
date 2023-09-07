from locust import HttpUser, task, between
from gevent.pool import Group


num_of_parallel_requests = 6


class User(HttpUser):
    wait_time = between(0.05, 0.1)
    url = '/app/public'

    @task(1)
    def test_api(self):
        group = Group()
        for i in range(0, num_of_parallel_requests):
            group.spawn(lambda: self.client.get(self.url))
        group.join()

# from locust import HttpUser, task, between
#
#
# class User(HttpUser):
#     wait_time = between(0.05, 0.1)
#     url = '/app/public]'
#
#     @task(1)
#     def test_api(self):
#         self.client.get(self.url)
