from conversions.encode.ByteArrayToNumericBase import ByteArrayToNumericBase


class ByteArrayToHex(ByteArrayToNumericBase):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, 16)
