import abc
from typing import Optional

from models.params_info import ParamsInfo


class XToY(abc.ABC):
    FROM_UNICODE = 0
    TO_UNICODE = 1
    OTHER_CONV = 2

    """
    parameters:
    Please supply a list of 
    """

    def __init__(self, val, parameters=None, _type=OTHER_CONV):
        self.val = val
        self.parameters = parameters
        self._type = _type

    @abc.abstractmethod
    def transform(self):
        pass

    def get_type(self) -> int:
        return self._type

    def has_params(self):
        return self.parameters is not None

    @staticmethod
    def uses_params():
        return False  # Only classes which have parameters should set this to True.

    """
    Get info on parameter accepted.
    Will be returned as an object.
    Info must be of type ParamsInfo.
    """
    @staticmethod
    def param_info() -> Optional[ParamsInfo]:
        return None