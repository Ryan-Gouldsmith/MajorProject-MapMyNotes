"""
Based upon the Tutorial here. Flask out of the box does not give the migrations, but Migrations would be useful for this application
https://flask-migrate.readthedocs.org/en/latest/ and
https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
This script has been modified to run with Postgresql and import the database from __init__.py of MapMyNotesApplication


Run initialises all the migrations directory and that's not my own - but the scripts auto-generated version.
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from MapMyNotesApplication import application, database


application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mapmynotes'

migate = Migrate(application, database)
manager = Manager(application)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
