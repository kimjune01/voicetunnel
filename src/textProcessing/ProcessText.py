class ProcessText(object):
    """
    Class of text processing methods in python
    """
    @staticmethod
    def isSelfIdentification(userInput):

        return True

    @staticmethod
    def isUserMessaging(userInput):
        return True

    """
        take in a string like "Hi I'm June"
        or "my name is June" <
        and extract the name
        will need NLP properly here
    """

    @staticmethod
    def getUserName(userInput):
        if userInput is None or "": return None
        print("getUserName: ", userInput)
        # assume that the last word of userInput
        inputlist = userInput.split()
        recipientName = inputlist[-1].lower()
        return recipientName

    '''
    method to check if string indicates we are running
    the client via testing mode
    '''
    @staticmethod
    def checkTestingMode(str):
        inputList = str.split()[0]
        return inputList == "TEST_MODE:"

    @staticmethod
    def isAffirmative(userInput):
        inputList = userInput.split()
        affirmativeList = ['yes', 'yep', 'ya', 'yeah', 'correct', 'right', 'yah', 'maybe', 'may be']
        for word in inputList:
            if word in affirmativeList:
                return True
        return False

    """
        take in a string: "hey june can you pick up some cheese"
        Understand the hey and name, extract name and message
        will need NLP properly here
    """
    @staticmethod
    def getNameandMessage(userInput):
        # TODO More sophis later on
        inputList = userInput.split()
        recipientName = inputList[1].lower()
        message = ' '.join(inputList[2:])
        return recipientName , message

    @staticmethod
    def hasNameandMessage(userInput):
        #TODO More sophis later on
        inputList = userInput.split()
        if len(inputList) < 2:
            return False
        else:
            return True

    @staticmethod
    def hasRecipientName(userInput):
        targetPhrase = ['yo', 'yah', 'hey']
        return any (phrase in userInput.split() for phrase in targetPhrase)
