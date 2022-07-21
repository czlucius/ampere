from main.conversions.encode.ByteArrayToNumericBase import ByteArrayToNumericBase


class ByteArrayToHex(ByteArrayToNumericBase):
    def __init__(self, val):
        super().__init__(val, 16)
