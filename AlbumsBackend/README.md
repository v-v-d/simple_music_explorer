Simple Music Explorer Albums microservice
=======

Simple Music Explorer Albums is a Flask application that creates a RESTful 
backend to store music in album format.

Set it up
------

Create a virtual environment and install the requirements on:

Linux

    $ python3 -m venv ./venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt
    
Windows

    $ py -m venv ./venv
    $ venv/Scripts/activate
    $ pip install -r requirements.txt


Get the local database ready

    $ python init_db.py

Start the development server

    $ FLASK_APP=wsgi.py flask run
    * Serving Flask app "wsgi.py"
    * Environment: production
    WARNING: Do not use the development server in a production environment.
    Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Check the service at http://127.0.0.1:5000/


Tests
------

Run the unit tests with

    $ pytest


Dependencies
------

Simple Music Explorer Albums uses Flask as a web framework, Flask RESTplus 
for creating the interface, and SQLAlchemy to handle the database models. 
It uses a SQLlite database for local development.
