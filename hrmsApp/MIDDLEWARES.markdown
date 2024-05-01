A middleware is a regular Python class that hooks into Django's resquest/response lifecycle. Those classes hold pieces of code that are processed upon every request/response your Django application handles.

Django provides 2 different ways to implement middlewares- a class-based approach and a function-based approach. In the function-based approach, we write a django factory callable that takes a __get_response__ callable and returns a middleware. A middleware is a callable that takes a request and returns a response, just like a view. Middleware classes are written such that its instances are callables.

A class-based middleware approach is more frequently used than a function-based one.

In this project I will be using class-based middleware:

`
class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        #one time configuration/initialization

    def __call__(self, request):
        #code to be executed for each request before the view or a later middleware is called

        response = self.get_response(request)

        #code to be executed for each request/response after the view is called

    return response
`

1. When the class is instantiated it is going to run the initialization method, __init__. __init__() method is called only once when the web server starts, unlike __call__() which method which is called once per request.
2. __call__ method, this is where we set up the middleware to perform actions. Before the view or any other middleware is called this is where we perform logic. 
3. Update this middleware class in the MIDDLEWARE list in your settings.py. THE ORDER OF THE MIDDLEWARE MATTERS BECAUSE A MIDDLEWARE CAN DEPEND ON ANOTHER MIDDLEWARE. For example, authentication middleware stores the authenticated user in the session, therefore, it must run after SessionMiddleware.
4. get_response is a callable which might be the next middleware in the chain of middlewares or the actual view in case it is the last listed middleware.

Django middleware hooks:
1. Django middleware class has two required methods __init__ and __call__
2. three optional methods that execute at different points of the view request/response life-cycle.
3. Called during request:
    * process_request(request)
    * process_view(request, view_func, view_args, view_kwargs): provides access to the view before the request hits the view. Here we can perform checks before it hits the view.
4. Called during response:
    * process_exception(request, exception): only if the view raised an exception
    * process_template_response(request, response): only if the view raised an exception.
    * process_response(request, response)