# models.py
# created by James L 07/07/2017

# file for all our database related python objects, used for ORM

from src.app_file import db

class User(db.Model):
    """The test case table in mera_db"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    socketInstanceId = db.Column(db.String(60)) # to store the uuid that maps to a websocket instance


    def __init__(self, name):
        self.name = name

    def getSocketInstanceId(self):
        return self.socketInstanceId

    def setSocketInstanceId(self, socketInstanceId):
        self.socketInstanceId = socketInstanceId
