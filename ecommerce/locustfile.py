from locust import HttpUser, task, between

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4NTM1MjkyLCJpYXQiOjE3Nzg1MzE2OTIsImp0aSI6IjQ5NWM4ODIyOGMxZDQxYTdiMjRiMTFlMDg4NjliZWQ4IiwidXNlcl9pZCI6IjMifQ.9x_eweSTtkJ3UOi0BCUIDyPxebjmMshrxDCcymLSWac"


class EcommerceUser(HttpUser):

    wait_time = between(1, 2)

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    @task
    def create_order(self):

        self.client.post(
            "/api/orders/",
            json={
                "product_id": 1,
                "quantity": 1
            },
            headers=self.headers
        )

    @task
    def pay_order(self):

        self.client.post(
            "/api/orders/1/pay/",
            headers=self.headers
        )