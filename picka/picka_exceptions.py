class InvalidRange(ValueError):
    """Raise when a specific subset of values in context of app is wrong"""
    def __init__(self, message, *args):
        self.message = message
        super(InvalidRange, self).__init__(message, *args)

