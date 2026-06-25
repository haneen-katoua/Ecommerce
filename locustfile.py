# from queue import Empty, Queue
# from locust import HttpUser, between, task
# #هون استخدمت الطابور مشان اضمن انو كل مستخدم وهمي عم ياخد حساب حقيقي وفريد 
# user_queue = Queue()
# for i in range(1, 100):
#     user_queue.put((f"user_clean100_{i}", "testpass123"))

# class EcommerceUser(HttpUser):
#     wait_time = between(1, 3)

#     def on_start(self):
#         self.token = None
#         self.headers = {}

#         try:
#             username, password = user_queue.get_nowait()
#         except Empty:
#             print("انتهت الحسابات المتاحة في الطابور!")
#             return

#         with self.client.post(
#             "/api/login/",
#             json={"username": username, "password": password},
#             catch_response=True,
#         ) as response:
#             if response.status_code == 200:
#                 self.token = response.json().get("access")
#                 self.headers = {"Authorization": f"Bearer {self.token}"}
#                 response.success()
#             else:
#                 response.failure(f" فشل تسجيل دخول {username}: كود {response.status_code}")

#     @task(3)
#     def products(self):
#         if self.token:
#             self.client.get("/api/products/", headers=self.headers)

#     @task(2)
#     def top_products(self):
#         if self.token:
#             self.client.get("/api/top-products/", headers=self.headers)

#     @task(2)
#     def checkout(self):
#         if self.token:
#             self.client.post(
#                 "/api/checkout/",
#                 json={"product_id": 1, "quantity": 1},
#                 headers=self.headers,
#             )

#     @task(1)
#     def create_order(self):
#         if self.token:
#             self.client.post(
#                 "/api/orders/",
#                 json={"product_id": 1, "quantity": 1},
#                 headers=self.headers,
#             )


from queue import Empty, Queue
from locust import HttpUser, between, task
import gevent
user_queue = Queue()

for i in range(1, 500):
    user_queue.put((f"user_saratest15_{i}", "testpass123"))

class EcommerceUser(HttpUser):

    wait_time = between(1, 3)

    def on_start(self):
        
        self.headers = {}
        self.current_user = None
        self.authenticated = False

        try:
            self.current_user = user_queue.get_nowait()
        except Empty:
            print(" Warning: User queue is completely empty!")
            return

        username, password = self.current_user

        with self.client.post(
            "/api/register/",  
            json={"username": username, "password": password, "email": f"{username}@test.com"},
            catch_response=True,
        ) as reg_response:
            if reg_response.status_code in [200, 201, 202]:
                reg_response.success()
            else:
                reg_response.failure(f" Registration failed for{username}: {reg_response.status_code}")
                user_queue.put(self.current_user)
                return

        gevent.sleep(0.2)

        max_retries = 3
        for attempt in range(max_retries):
            with self.client.post(
                "/api/login/",
                json={"username": username, "password": password},
                catch_response=True,
            ) as login_response:
                if login_response.status_code == 200:
                    token = login_response.json().get("access")
                    self.headers = {"Authorization": f"Bearer {token}"}
                    login_response.success()
                    self.authenticated = True
                    print(f" User logged in successfully: {username} on attempt {attempt + 1}")
                    break 
                else:
                    if attempt < max_retries - 1:
                        login_response.success() 
                        gevent.sleep(0.5)
                    else:
                        login_response.failure(f" Final login failed for {username}: {login_response.status_code}")
                        user_queue.put(self.current_user)


    @task(3)
    def products(self):
        if self.authenticated:
            self.client.get("/api/products/", headers=self.headers)

    @task(2)
    def top_products(self):
        if self.authenticated:
            self.client.get("/api/top-products/", headers=self.headers)

    @task(2)
    def checkout(self):
        if self.authenticated:
            self.client.post(
                "/api/checkout/",
                json={"product_id": 1, "quantity": 1},
                headers=self.headers,
            )

    @task(1)
    def create_order(self):
        if self.authenticated:
            self.client.post(
                "/api/orders/",
                json={"product_id": 1, "quantity": 1},
                headers=self.headers,
            )