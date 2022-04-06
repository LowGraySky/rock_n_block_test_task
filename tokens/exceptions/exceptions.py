class EmptyParamError(ValueError):

    def __init__(self, param: str):
        self.param = param

    def _get_message(self):
        message = "'{}' shouldn't be empty or None".format(self.param)
        return message

    message = property(
        fget=_get_message
    )
