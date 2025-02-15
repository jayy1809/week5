from locust import HttpUser, task, between
from faker import Faker

fake = Faker()

class FastAPIUser(HttpUser):
    wait_time = between(1, 2)  # Random wait time between requests

    # @task
    # def test_root(self):
    #     self.client.get("/")  # Replace with your FastAPI API endpoint

    # @task
    # def test_create_user(self):
    #     data = {"username": "testuser", "password": "password123"}
    #     self.client.post("/users/", json=data)  # Replace with your API route
    @task
    def test_example_point(self):
        payload = {
                    "name": fake.name(), 
                    "email": fake.email(), 
                    "address": fake.address()
                }
        self.client.post("/api/example", json = payload)

    @task
    def test_get_products(self):
        self.client.get("/api/request")  # Replace with your API route
