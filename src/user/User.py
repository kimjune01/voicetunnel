from enum import Enum

class UserState(Enum):
    Nameless = 0
    NameStaging = 1
    Ready = 2
    Conversing = 3
    Invalid = 99

class User(object):

    socket = None
    name = None
    state = UserState.Nameless
    conversant = None

    """docstring for User"""
    def __init__(self):
        super(User, self).__init__()

    def setState(self, newState):
        self.state = newState
        print("User {} is now in state {}".format(self.name, self.state))
    

