class PhoneError(Exception):
    ...

class InavlidQuantyPassword(Exception):
    ...

class KeyErrorUser(Exception):
    ...
class EmailErro(Exception):
    ...
class BadRequestError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.code = 400

class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.code = 404
