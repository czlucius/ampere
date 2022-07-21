from main.conversions import XToY


class TextToByteArray(XToY):
    def transform(self):
        return bytes(self.val, encoding="utf-8")

    def get_type(self) -> int:
        return self.FROM_UNICODE
