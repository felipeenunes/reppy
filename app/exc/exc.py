class PhoneError(Exception):
    ...
class NonAuthorizedError(Exception):
    ...
class InvalidQuantityPassword(Exception):
    ...

class KeyErrorUser(Exception):
    ...
class EmailError(Exception):
    ...
class BadRequestError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.code = 400

class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.code = 404

class InvalidZipCode(Exception):
    ...

class InvalidStateInitial(Exception):
    ...

class InvalidKeys(Exception):
    ...

class MissingKeys(Exception):
    ...

class InvalidValue(Exception):
    ...