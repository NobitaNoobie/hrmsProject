A middleware is a regular Python class that hooks into Django's resquest/response lifecycle. Those classes hold pieces of code that are processed upon every request/response your Django application handles.

Django provides 2 different ways to implement middlewares- a class-based approach and a function-based approach. In the function-based approach, we write a django factory callable that takes a __get_response__ callable and returns a middleware. A middleware is a callable that takes a request and returns a response, just like a view. Middleware classes are written such that its instances are callables.

A class-based middleware approach is more frequently used than a function-based one.

In this project I will be using class-based middleware:

```
class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        #one time configuration/initialization

    def __call__(self, request):
        #code to be executed for each request before the view or a later middleware is called

        response = self.get_response(request)

        #code to be executed for each request/response after the view is called

        return response
```

1. When the class is instantiated it is going to run the initialization method, __init__. __init__() method is called only once when the web server starts, unlike __call__() which method which is called once per request.
2. __call__ method, this is where we set up the middleware to perform actions. Before the view or any other middleware is called this is where we perform logic. 
3. Update this middleware class in the MIDDLEWARE list in your settings.py. THE ORDER OF THE MIDDLEWARE MATTERS BECAUSE A MIDDLEWARE CAN DEPEND ON ANOTHER MIDDLEWARE. For example, authentication middleware stores the authenticated user in the session, therefore, it must run after SessionMiddleware.
4. get_response is a callable which might be the next middleware in the chain of middlewares or the actual view in case it is the last listed middleware.

Django middleware hooks:
1. Django middleware class has two required methods __init__ and __call__
2. three optional methods that execute at different points of the view request/response life-cycle.
3. Called during request:
    * process_request(request)
    * process_view(request, view_func, view_args, view_kwargs): provides access to the view before the request hits the view. Here we can perform checks before it hits the view. It should return either None or an HttpResponse object. If it returns None, Django will continue processing this request, executing any other process_view() middleware and, then, the appropriate view. If it returns an Response object, then view will not be called at all.
4. Called during response:
    * process_exception(request, exception): only if the view raised an exception. Should return None or a Response object.
    * process_template_response(request, response): only if the view raised an exception.
    * process_response(request, response)



HOW DOES A CHAIN OF MIDDLEWARES WORK?
THE ROLE OF get_response():

Suppose we defined 3 middlewares:

`MIDDLEWARE = [....,
            hrmsApp.middleware.FirstMiddleware,
            hrmsApp.middleware.SecondMiddleware,
            hrmsApp.middleware.ThirdMiddleware]`

This order is important.

Three classes for 3 middlewares are defined in middleware.py file, likeso:

```
class FirstMiddleware:
    def __init__(self, get_response):
        get_response = self.get_response
        print("First Middleware initialization)

    def __call__(self, request):
        print("Before First view")
        response = self.get_response(request) #this takes it to the SecondMiddleware's __call__()method
        print("After First View")
        return response```

```class SecondMiddleware:
    def __init__(self, get_response):
        get_response = self.get_response
        print("Second Middleware initialization)

    def __call__(self, request):
        print("Before Second view")
        #response = self.get_response(request)
        print("After Second View")
        return response
```

Note that for SecondMiddleware, we do not get_response, this means that, the next middleware in chain, namely ThirdMiddleware, is not referenced at all. Check how the order of printing takes place.

```
class ThirdMiddleware:
    def __init__(self, get_response):
        get_response = self.get_response
        print("Third Middleware initialization)

    def __call__(self, request):
        print("Before Third view")
        response = self.get_response(request)
        print("After Third View")
        return response
```

When we run the server, the following is printed in the console:

`
Third Middleware initialization
Second Middleware initialization
First Middleware initialization
Before First View
Before Second View
After Second View
After First View
`

get_response is called just like nested functions. Note that the ThirdMiddleware is not called at all. This is because it was not nested within SecondMiddleware because we did not use the get_response.


WHAT IS TEMPLATE RESPONSE?
Template Response is a subclass of SimpleTemplateResponse that knows about the current HttpRequest.
