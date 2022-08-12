import abc


class XToY(abc.ABC):
    FROM_UNICODE = 0
    TO_UNICODE = 1
    OTHER_CONV = 2

    """
    parameters:
    Please supply a list of 
    """

    def __init__(self, val, input_params=None, output_params=None, _type= OTHER_CONV):
        self.val = val
        self.input_params = input_params
        self.output_params = output_params
        self._type = _type

    @abc.abstractmethod
    def transform(self):
        pass

    def get_type(self) -> int:
        return self._type

    def has_params(self):
        return bool(input_params or output_params)
    
