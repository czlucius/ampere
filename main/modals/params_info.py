"""
A simple object to store info for parameters.
"""
from discord import InputTextStyle


class ParamsInfo:
    def __init__(self, name: str,
                 placeholder: str = None,
                 min_length: int = None,
                 max_length: int = None,
                 required: bool = True,
                 prefilled_value: str = None,
                 style: InputTextStyle = InputTextStyle.short):
        self.name, self.style, self.placeholder, self.min_length, self.max_length, self.required, self.prefilled_value \
            = name, style, placeholder, min_length, max_length, required, prefilled_value