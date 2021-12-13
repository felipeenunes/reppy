class NonAuthorizedError(Exception):
    ...

class KeyErrorUser(Exception):
    ...

class BadRequestError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.code = 400 

class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.code = 404

class BadRequestWithDeleteError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.code = 400
