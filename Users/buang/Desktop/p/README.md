# WIT
Web Interactive Tutorial

Use  python3 and MySQL


1. Install requirements

$ pip install -r requirements.txt

2. Setup db

$ mysql -u root -p
# Enter password
mysql> CREATE DATABASE flask_todo_app;
mysql> source schema.sql;

3. Start server.

$ python3 run.py