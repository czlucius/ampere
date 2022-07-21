from main.conversions.decode.NumericBaseToByteArray import NumericBaseToByteArray


class HexToByteArray(NumericBaseToByteArray):
    def __init__(self, val):
        super().__init__(val, 2, r"[\da-f]", 16)
