============
URLShortener
============
.. image:: https://github.com/RaRhAeu/URLShortener/workflows/build/badge.svg
  :alt: Build status
  :target: https://github.com/RaRhAeu/URLShortener/actions?query=workflow%3Abuild

.. image:: https://codecov.io/gh/RaRhAeu/URLShortener/branch/master/graph/badge.svg
  :alt: Code coverage
  :target: https://codecov.io/gh/RaRhAeu/URLShortener

.. image:: https://img.shields.io/github/license/RaRhAeu/URLShortener
  :alt: License
  :target: https://github.com/RaRhAeu/URLShortener/blob/master/LICENSE


-----------------------------
Yet another url-shortener API
-----------------------------
Introduction
------------
This is simple url-shortener api, based on python and depends on the following major componets:
 - Flask - Web application microframework for Python
 - PostgreSQL - Database
 - SQLAlchemy - ORM framework
 - Redis - Caching
 - Celery - Background tasks
 - Pytest - Unit test framework

.....
About
.....
Although the idea is quite easy, this project is aimed at the following goals:
 - Getting basic knowledge about Flask
 - Proper project structure and setup
 - Implementing third party services such as Caching (Redis) and background tasks (Celery)
 - Securing API the proper way, without violating the REST principles (token based auth)
 - Writing some unit test with pytest framework
 - Containerizing app with docker and configuring for production with gunicorn

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

Todos status:
.............
 - Create CRUD API for managing urls [+]
 - Create CRUD API for managing users [+/-]
 - Add user authentication and authorization (Flask-JWT + Bcrypt) [-]
 - Implement CORS policy [+]
 - Create caching mechanism using Redis [+/-]
 - Implement Celery worker [-]
 - Write tests [+/-]
 - Containerize app with Docker [-]
 - Configure CI with Github Actions (Lint, Test + Codecov) [+]
 - Add QR Code generating endpoint [-]
 - Add logging [-]