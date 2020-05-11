class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class AuthError(Exception):
    def __init__(self, message):
        self.message = message

class NoCachedTokenError(AuthError):
    def __init__(self):
        super(NoCachedTokenError, self).__init__('No cache token was found. Please sign out and sign in agin.')