from main.conversions.encode.ByteArrayToNumericBase import ByteArrayToNumericBase


class ByteArrayToBinary(ByteArrayToNumericBase):
    def __init__(self, val):
        super().__init__(val, 2)
