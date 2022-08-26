from components.conversions.encode.ByteArrayToNumericBase import ByteArrayToNumericBase


class ByteArrayToBinary(ByteArrayToNumericBase):
    def __init__(self, val, *args, **kwargs):
        super().__init__(val, 2)
