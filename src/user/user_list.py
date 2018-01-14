class UserList(object):
  __instance = None
  users = []
  def __new__(cls):
    if UserList.__instance is None:
        UserList.__instance = object.__new__(cls)
    return UserList.__instance
  
  #happens on connection
  @classmethod
  def append(cls, user):
    cls.users.append(user)

  @classmethod
  def setNameforSocket(cls, name, socket):
    # TODO: make this search faster somehow???
    for u in cls.users:
      if u.socket == socket:
        u.name = name
        return True
    return False

  @classmethod

  def userFromName(cls, name):
    # assume no name conflicts...
    users = [each for each in UserList.users if each.name == name]
    return users[0] if users else None

  @classmethod
  def userFromSocket(cls, socket):
    for u in cls.users:
      if u.socket == socket:
        return u
    return None

  @classmethod
  def deleteUserBySocket(cls, socket):
    for i in range(len(cls.users) - 1):
      if cls.users[i].socket == socket:
        del cls.users[i]

  @classmethod
  def containsUser(cls, user):
    for u in cls.users:
      if u == user:
        return True
    return False

