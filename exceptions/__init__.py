class InvalidExpressionException(Exception):
    pass

class TimeoutException(Exception):
    pass

class FieldTooLongError(Exception):
    pass

class InputInvalidException(Exception):
    pass

class EncodeDecodeError(Exception):
    pass

class InvalidParametersException(InputInvalidException):
    pass

class CipherError(Exception):
    pass

class CodeRunnerException(Exception):
    pass
