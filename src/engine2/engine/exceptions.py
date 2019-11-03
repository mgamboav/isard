class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class NotFoundError(Error):
    def __init__(self, id, message):
        self.id = id
        self.message = message

class TransitionError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message
