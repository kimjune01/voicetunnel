from tornado.websocket import WebSocketHandler
from textProcessing.ProcessText import ProcessText
from asynchronous.countdown import EventLoop, Countdown
from user.User import User, UserState
from user.user_list import UserList

DURATION_CONST = 20

class WebSocket(WebSocketHandler):

    eventLoop = None
    countDown = None

    '''
    Crucial methods to WebSocket class
    '''
    def check_origin(self, origin):
        return True

    def open(self):
        print("SERVER: On new connection!")
        newUser = User()
        newUser.socket = self
        UserList.append(newUser)

        self.askForName()

    def on_message(self, str):
        if str == "ping": return
        #TODO: get user instance, given socket
        print("on_message: ", str)
        # guard
        testing = ProcessText.checkTestingMode(str)

        user = self.currentUser()
        if testing:
            print("SERVER: In testing mode")
            name = ProcessText.getUserName(str)
            user.name = name
            user.setState(UserState.Ready)

        if user is None:
            self.write_message('Fatal Error, user is None')
            return
        state = user.state
        if state is UserState.Invalid:
            self.write_message('Invalid state, start over')
            return

        if state is UserState.Nameless:
            self.handleNamelessState(user, str)
        elif state is UserState.NameStaging:
            self.handleNameStagingState(user, str)
        elif state is UserState.Ready:
            self.handleReadyState(user, str)
        elif state is UserState.Conversing:
            self.handleConversingState(user, str)
        else:
            self.write_message('Invalid state, start over')
        return

    def on_close(self):
        user = self.currentUser()
        UserList.deleteUserBySocket(user.socket)
        print("Socket closed.")

    '''
    Helper methods to websocket class
    TODO: refactor to make less heavy
    '''

    def currentUser(self):
        return UserList.userFromSocket(self)

    def askForName(self):
        print("askForName")
        self.write_message("State your name")

    def handleNamelessState(self, user, str):
        name = ProcessText.getUserName(str)
        if name is not None:
            # self.eventLoop = EventLoop(lambda: self.confirmName(name))
            # self.eventLoop.start()
            self.confirmName(name)
            user.setState(UserState.NameStaging)
        else:
            self.askForName()

    def confirmName(self, name):
        self.write_message(f"Is your name {name}?")
        user = self.currentUser()
        user.name = name
        user.setState(UserState.NameStaging)

    def handleNameStagingState(self, user, str):
        # empty string case also handled by client
        if not str:
            # self.eventLoop = EventLoop(lambda: self.confirmName(user.name))
            # self.eventLoop.start()
            self.confirmName(user.name)
            return

        # self.clearEventLoop()
        if ProcessText.isAffirmative(str):
            user.setState(UserState.Ready)
            self.write_message(f"Hello {user.name}, now ready to send messages")
        else:
            user.setState(UserState.Nameless)
            self.askForName()

    def handleReadyState(self, user, str):
        #check existence of name and message
        if not ProcessText.hasNameandMessage(str):
            self.write_message("who is the recipient and what is the message")
            return

        recipientName, message = ProcessText.getNameandMessage(str)
        if not message:
            # message body is empty, just copy whole input to message
            message = str

        recipient = self.messageNamedUser(user, recipientName, message)
        # then in this block, if success, start countdown for both users
        if recipient:
            user.setState(UserState.Conversing)
            # when timer runs out, setState to UserState.Ready
            self.countDown = Countdown(lambda: user.setState(UserState.Ready), duration=DURATION_CONST)
            recipient.socket.countDown = Countdown(lambda: recipient.setState(UserState.Ready), duration=DURATION_CONST)
            self.countDown.start()
            recipient.socket.countDown.start()

    def messageNamedUser(self, user, recipientName, message):
        if not recipientName:
            self.write_message("could not recognize the recipient in your message")
            return
        recipient = UserList.userFromName(recipientName)
        if not recipient or not recipient.socket:
            self.write_message("could not find {}".format(recipientName))
            return

        # terminate conversation on other end if switching to new recipient
        if user.conversant is not None and user.conversant != recipient:
            user.conversant.conversant = None
            user.conversant.state = UserState.Ready

        # handle multi way conversation between users
        user.conversant = recipient
        recipient.conversant = user
        recipient.state = UserState.Conversing

        recipient.socket.write_message(f"{user.name} says, {message}")
        return recipient

    def handleConversingState(self, user, str):
        print("handleConversingState user: {}".format(user.name))
        self.restartCountDown(user, user.conversant)
        if ProcessText.hasRecipientName(str):
            recipientName, message = ProcessText.getNameandMessage(str)
            if not message:
                message = str
            self.messageNamedUser(user, recipientName, message)
        else:
            user.conversant.socket.write_message(str)

    def restartCountDown(self, user, recipient):
        # cancels the previous countDown,
        print("COUNTDOWN: Stopping previous thread")
        if self.countDown:
            self.clearCountDown(self)

        if recipient.socket.countDown:
            self.clearCountDown(recipient.socket)

        # restart countDown
        print("restartCountDown: making new instance")
        self.countDown = Countdown(lambda: user.setState(UserState.Ready), duration=DURATION_CONST)
        recipient.socket.countDown = Countdown(lambda: recipient.setState(UserState.Ready), duration=DURATION_CONST)
        recipient.socket.countDown.start()
        self.countDown.start()

    def clearEventLoop(self):
        self.eventLoop.stop()
        self.eventLoop = None

    def clearCountDown(self, socket):
        socket.countDown.stop()
        socket.countDown = None
