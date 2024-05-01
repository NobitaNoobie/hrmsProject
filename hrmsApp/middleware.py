from typing import Any

# boiler plate middleware
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("This code excecutes only once when server starts at the beginning/initializing")

    def __call__(self, request):
        print("Excecutes once per request")
        print("This is before view")
        response = self.get_response(request)
        print("This is after view")
        return response
