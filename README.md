# description of the server with which we interact with the database

The parts of project
- `app.py ` - server code
- `database.py ` is the code of functions accessing the database. The functions of this file should be called from the functions`app.py `.

Thus, we will consider the server as the entry point to the application, and the functions interacting with the database as auxiliary ones that are used at the entry point where necessary.

You should also install the following packages:
```
pip install SQLAlchemy
pip install psycopg2
```
