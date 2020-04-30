============
URLShortener
============
----------------------------------------------------
Yet another url-shortener API made with python Flask
----------------------------------------------------
Introduction
------------
This is simple url-shortener api, based on python and depends on the following major componets:
 - Flask - web application microframework for Python
 - PostgreSQL - Relational database managment system
 - SQLAlchemy - ORM framework
 - Redis - Caching
 - Celery - for background tasks
 - Pytest - unit test framework

..................
Getting the source
..................
``$ git clone https://github.com/RaRhAeu/URLShortener``

............
Installation
............
Pipenv
......
``$ sudo pip install pipenv``

``$ pipenv install --dev``

Postgresql
..........
Assuming you have postgres already installed

Change to the postgres user

``$ sudo su - postgres``

Create a database user account for yourself

``$ createuser -s <your username>``

Create skylines database with yourself as the owner

``$ createdb urlshortener -O <your username>``

Running the server
..................
``$ pipenv shell``

``$ python manage.py run``