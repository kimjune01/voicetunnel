# manage.py

import datetime
import time
from random import randint
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from src.app_file import db, create_app, config_name
from src import models

app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    '''
    Assumes you have already have sleeportant database
    db init, and upgrade the databases
    method to create some initial users locally and insert to database
    make sleep records for each user for a large date range ~100-200 days
    :return:
    '''
    print("Seeding database with initial users")
    user1 = models.User(name="Rick")
    user2 = models.User(name="Talia")
    user3 = models.User(name="Christina")
    sleepStateList = ["GOOD", "OKAY", "BAD"]


    db.session.add_all([user1, user2, user3])
    db.session.flush()
    db.session.commit()
    print("Users created!")
    print("Seeding database for users sleep records")
    return

if __name__ == '__main__':
    manager.run()