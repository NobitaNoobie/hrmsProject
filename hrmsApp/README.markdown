APP DOCUMENTATION:

****************1. REQUEST - RESPONSE FLOW***************

VIEW IN DJANGO:
1. A view is a python function that takes a Web Request as a parameter and returns a Web Response.

2. A view can be placed anywhere as long as it is in a Python path. Following the standard, we place the view functions in a __views.py__ file.

3. The view function has any name, and can contain any logic that is necessary to return a response. 

4. The Response can be an HTTP response of any form(an HTML webpage, a 404 page, an image, a simple text, a JSON, etc.).

5. Now that we have defined a view function which returns a Response, we need something to display the Response. We display this view at a particular URL, by creating a URLcong in __urls.py__ file.

Notes: __urls.py__ will be explained in later sections.

Basic structure of a view:---------------------------

STEP 1:
here, index() is a views function.
__hrmsApp/views.py__:
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world!")

STEP 2:
__hrmsApp/urls.py__:
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name ="index"),
]

STEP 3:
Point the root URLconf at the hrmsApp.urls module. 
__hrmsProject/urls.py__:
from django.contrib import admin
from django.urls import include, path

urlPatterns = [
    path("hrmsIndex/", include(hrmsApp.urls)),
    path("admin/", admin.site.urls),
]

The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched upto that point and sends the remining string to the included URLconf for further processing.

Notes:
You should always use include() when you includeother URL patterns. admin.site.urls is the only exception to this.

In this example, you have now wired an index view into the URLconf. Verify its working with the following command:
    py manage.py runserver


__urls.py__:------------------------------------------
urlpatterns[] is an array which contains one or more 'path()' functions as array elements.

The basic pattern of an url pattern array element is:
path("pathName/", views.functionName, name="Some name", kwargs)

The path() functions passes 4 arguments: route, view function, name and kwargs. route and view are mandatory.

1. route -> a string ; contains a url pattern or endpoint ; "endpointName/"
2. view -> view Django finds a matching url pattern, it calls the specified view function with an HttpRequest object as the first argument.
3. kwargs -> Arbitrary keyword arguments can be passed in a dictionary to the target view. 
4. name -> an attribute which has a string value, lets you name the URL and access it from elsewhere in django


*******************2. Database setup**********************

1. hrmsProject/settings.py: it is a normal Python module with module-level variables representing Django variables.

2. By default the configuration uses SQLite.

3. Since we are using MySQL as the primary database, we need to change the deafult database settings in the settings.py file and install appropriate database drivers because Django use SQLite as a database in backend. In the official docs, they recommend using databases other than SQLite if you plan to host your project to production.

    STEP 1: 
    pip install mysqlclient in the project directory
this installs thedriver needed for running mysql, namely mysqlclient

    STEP 2: 
change the following keys in the DATABASES 'default' item to match your database connection settings:
ENGINE- 'django.db.backends.mysql'
NAME- Name of your database.

DATABASES is a nested dictionary

1. ENGINES settings changed.
2. Granted create database priviledges by running command GRANT ALL ON *.* TO 'root'@'localhost' WITH GRANT OPTION
3. Then verified the priviledges granted by running the command SHOW GRANTS FOR 'root'@'localhost'
4. The list of apps in the INSTALLED APPS settings holds tha name of all Django apps that are activated in this Django instance(including the hrmsApp which will be included manually in the INSTALLED APPS settings). Some of these apps(including our own hrmsApp) uses atleast one table in the database. So we need to create the tables in database so that these apps can use them. To do so run the command: 
        py manage.py migrate
5. The using command SHOW TABLES (screenshot attached) we see the tables that django has created for the apps listed in the INSTALLED APPS settings.


DEFINE A DATA MODEL--------------------------------

Definition: A model is a single, definitive source of information about your data. It contains the essential fields and behaviours of the data you're storing. 

1. Each model is represented by Python classes.
2. These classes are written in the __hrmsApp/models.py__ file
3. CAUTION: Naming standard: use lowercase letters and underscored to separate words, example, employee_id
4. All schema fields are represented as objects of different Field classes.

This model definition helps Django to:
1. create a database table for this app
2. create a pyhton database-access API for accessing the class(schema) Objects.


NEXT STEP: To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. The HrmsAppConfig class is in the hrmsApp/apps.py file, so its dotted path is 'hrmsApp.apps.HrmsAppConfig'. Edit the hrmsProject/settings.py file and add that dotted path to the INSTALLED_APPS setting. 


------------------------
************************
Notes: AFTER MAKING ANY CHANGES TO THE SCHEMA RUN THE FOLLOWING COMMAND:

__STEP 1__:
        py manage.py makemigrations appName

What this does?
Django creates a table for LeaveApplication schema, named hrmsApp_leaveapplication

You can read the migration for your new model if you like; it’s the file hrmsApp/migrations/ files


__STEP 2__: 
        py manage.py check

__STEP 3__:
        py manage.py migrate

**********************************************************
******************** WRITING APIs THAT DO SOMETHING*******

__hrmsApp/views.py__:
    we will change the employeehome function
    this time the function will have an additional parameter.

    def employeehome(request, employee_id):
        response = "Hi %s! Welcome to your leave application portal"
        return HttpResponse(response % employee_id)

make corresponding changes in the urls:
__hrmsApp/urls.py__:

-----------------------------------------------
* path("employeeHome/<str:employee_id>", views.employeehome, name="employee_home")

* def employeehome(request, __employee_id__):
    response = "Hello %s! Welcome to your leave application portal" % employee_id
    return HttpResponse(response)

__Notes__: using angle brackets "captures" part of the URL and sends it as a keyword argument to the view function employee_home

* The employee_id part of the string defines the name that will be used to identify the matched pattern, and the 
* 'str' part is a converter that determines what patterns should match this part of the URL path.
* The colon(:) separates the converter and pattern name.
Notes: Each view is responsible for doing one of two things: returing an HttpResponse object containing the content for the requested page, or raising an exception such as Http404.


****************************************************************************Django middleware*************************

