py manage.py runserver -> for starting the development server
py manage.py runserver 8080 -> for changing the port 

HOW TO MAKE A NEW VIRTUAL ENVIRONMENT AND START A PROJECT IN THE ENVIRONMENT?
A virtual environment is an isolated Python environment that allows you to install packages and dependencies for your project without affecting the global Python installation on the system.

1. Check python installation:
	python --version
2. Install virtual environment:
	pip install virtualenv
3. If error, do the following:
	pip install --upgrade pip


HOW TO START THE PROJECT and WORK WITH THE venv?

1. firstly create django virtual environment
	python -m venv django-env
2. you need to activate this virtual environment
	cd django-env
	Scripts\activate
the vitual environment will be activated
3. cd..

this to navigate back to system user outside the virtual environment file because virtual environment is separated from the project. Refer below to learn 2 methods to structure virtual environment. Note that cd.. will take you out of the FOLDER of the virtual environment. To deactivate the virtual environment type 'deactivate'.

4. install django and other required packages inside this virtual environment you have created
	pip install django_rest_framework
	INSTALL DJANGO COMMAND: [py -m pip install Django]
5. check django version for installation
	django-admin --version
6. make a django project:
	django-admin startproject projectName
7. make a django app inside the project directory:
	cd projectName
	py manage.py startapp appName
8. need to register the django app as well as the REST framework
inside the INSTALLED APPS:
	['rest_framework',
	'appName',...]

2 WAYS TO STRUCTURE THE VIRTUAL ENVIRONMENT
1. Putting virtual env inside project. Separating environments for different projects.
2. Separating virtual env and deploy many projects using the same virtual environment. I prefer this method.




PROJECT STRUCTURE:
1. manage.py: a command line utility that lets you interact with this Django project in various ways. 

2. the inner hrmsProject\ directory: it is the actual Python pacakage of the project. Its name is the Python package name that will be used to import anything inside it, example, hrmsProject.urls

3. /__init__.py: an empty file that tells Python that this dirctory should be considered a Python package.

4. /settings.py: settings and configurations for the django project

5. /urls.py: It is a table of contents of all the urls or endpoints that will be used in this Django project.

6. /asgi.py: An entry-point for ASGI-compatible web servers to serve this project. 

7. /wsgi.py: An entry-point for WSGI-compatible web servers to serve your project.


HOW TO START THE DJANGO DEVELOPMENT SERVER?

Navigate to the project directory and write the following command to start the django development server:
    py manage.py runserver
    or
    py manage.py runserver 8080


by default the url is http://127.0.0.1:8000/

CTRL + C is used to exit the development server.

Notes: The Django development server is a lightweight WEB SERVER written in Python. Until ready for production server, like Apache, we have used this development server to develop things rapidly without having to worry about configuring things for production.


PROJECT VS APP
A project can contain multiple apps and an app can be a part of multiple projects.


Notes: In this project, we have created the hrmsApp in the same directory as manage.py file so that it can be imported as its own top-level module rather than a submodule of hrmsProject.

Notes: ROOT_URLCONF 

admin.py is optional register your models into this

CMD COMMANDS:---------------------------------------------

1. AFTER MAKING ANY CHANGES TO THE SCHEMA RUN THE FOLLOWING COMMAND:
        py manage.py makemigrations appName

2. AFTER MAKING ANY CHANGES IN CODE/WRITING AN API
		py manage.py runserver

3. THREE STEP GUIDE TO MAKING MODEL CHANGES:
		* Change your models (in __models.py__).
		* Run __python manage.py makemigrations__ to create migrations for those changes. To make migrations for a particular app in your project, run __python manage.py makemigrations appName__.
		* Run __python manage.py migrate__ to apply those changes to the database.

