import abc


class XToY(abc.ABC):
    FROM_UNICODE = 0
    TO_UNICODE = 1
    OTHER_CONV = 2

    def __init__(self, val, _type= OTHER_CONV):
        self.val = val
        self._type = _type

    @abc.abstractmethod
    def transform(self):
        pass

    def get_type(self) -> int:
        return self._type
