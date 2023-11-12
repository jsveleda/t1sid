import random
from locust import HttpUser, task, between

class VirtualUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 to 5 seconds between tasks

    @task(0)
    def access_read_route(self):
        key = f'key_{random.randint(0, 5000)}' 
        self.client.get(f"/read/{key}")

    @task(100)
    def acess_create_route(self):
        key = f'key_{random.randint(0, 5000)}' 
        value = str(random.randint(0, 5000))
        self.client.post(f"/create/{key}/{value}")

