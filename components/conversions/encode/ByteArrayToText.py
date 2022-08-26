from components.conversions import XToY


class ByteArrayToText(XToY):
    def transform(self):
        return self.val.decode("utf-8")

    def get_type(self) -> int:
        return self.TO_UNICODE
