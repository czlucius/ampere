
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def base_arb_to_bytes(s, base):
    v = int(s, base)
    b = bytearray()
    while v:
        # read first 8 bits
        b.append(v & 0xff)
        # shift 8 bits to read next 8 bits
        v >>= 8
    return bytes(b[::-1])


def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number ,base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)


def bytes_to_base_arb(by, base):
    v = ""
    for byte in by:
        v += (str_base(byte, base))
    return v
