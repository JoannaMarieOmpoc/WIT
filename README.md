Web Interactive Tutorial

Use python3 and MySQL

Install requirements

$ pip install -r requirements.txt

Setup db

$ mysql -u root -p Enter password mysql> CREATE DATABASE flask_todo_app; mysql> source schema.sql;

Start server.

$ python3 run.py