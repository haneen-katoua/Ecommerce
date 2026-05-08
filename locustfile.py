from locust import HttpUser, task, between
import random

TOKEN_LIST = [
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTU5Nzk2LCJpYXQiOjE3NzgxNTYxOTYsImp0aSI6ImYwZGVjOTIzYzhlMDQ3NTY5ODU1YzZhZjIyNDFlZjA4IiwidXNlcl9pZCI6IjQifQ.wfstSftvSOHfS6htRybtxKqDa7yH-9uBY3X5NIHQyEw", 
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTU5ODQ5LCJpYXQiOjE3NzgxNTYyNDksImp0aSI6IjkzN2UzZjgwOTJiYzQ3NzI5YjhlMjIzNzAxYzI3Mjg1IiwidXNlcl9pZCI6IjIifQ._aH_NM5yiBZ9RcsaLQTQV1XCceFUBf02jet_v-Ty_Jk",
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTU5OTAxLCJpYXQiOjE3NzgxNTYzMDEsImp0aSI6IjNkYzI2ZjU5ZDI3NDRlMGFiNzk1ZWRhNzcxNTQ2MmNhIiwidXNlcl9pZCI6IjMifQ.x33DSbWRA73D3lDDWhKd59kNTbwen3QgR7s0vzCGqyQ", 
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTU5OTIzLCJpYXQiOjE3NzgxNTYzMjMsImp0aSI6IjQ4ZmJiNWM3OGJhYzQ0OGQ5OTNmYjRkMTAyYzY4ODExIiwidXNlcl9pZCI6IjUifQ.FeBryI8VgNYGPkkb7kOOaa5h9F_1Z0i8-zapEzCVITA", 
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTU5OTYzLCJpYXQiOjE3NzgxNTYzNjMsImp0aSI6IjNjM2I1ZGY4MjEwZTRkMmFiOGY1M2NhNDgyZDQwNTgyIiwidXNlcl9pZCI6IjYifQ.-l85P5vn1hQFGwSqJd9NkDDtRJ27J7GHN9oL7EjvrEQ",
]

class RealWorldUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        if TOKEN_LIST:
            self.user_token = TOKEN_LIST.pop(0)
        else:
            self.user_token = None

    @task
    def access_products(self):
        if self.user_token:
            headers = {'Authorization': f'Bearer {self.user_token}'}
        #    self.client.get("/api/products/", headers=headers)
            self.client.get("/api/products/", headers=headers)