from locust import HttpUser, task, between


class RecommendUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_recommendation(self):
        self.client.get("/recommend/Smart")

    @task(2)
    def search_product(self):
        self.client.get("/search/gaming")

    @task(1)
    def home(self):
        self.client.get("/")
