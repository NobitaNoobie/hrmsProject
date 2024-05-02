from typing import Any

# boiler plate middleware
class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("This code excecutes only once when server starts at the beginning/initializing")

    def __call__(self, request):
        print("Excecutes once per request")
        print("This is before view")
        response = self.get_response(request) #writing this means it will go to next middleware or view in chain
        print("This is after view") #this will be printed only after all get_response have expired calling middlewares in the chain.
        return response

   
 