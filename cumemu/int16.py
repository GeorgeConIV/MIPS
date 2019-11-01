import copy

class Int16:
    def __init__(self, x):
        self.set(x)

    def set(self, x):
        if isinstance(x, Int16):
            self.set(x.actual)
        else:
            self.actual = max(min(x, 0x7FFF), -0x8000)
            self.val = abs(x) & 0x7FFF if x != -65536 else 65536
            self.n = True if x < 0 else False
            self.z = True if x == 0 else False
            self.c = True if (x & 0x10000) == 0 else False
            self.v = not self.c

    def bytes(self):
        return bytes([(self.actual & 0xFF00) >> 8, self.actual & 0xFF])

    def actualValue(self):
        return self.val * (-1 if self.n else 1)

    def __add__(self, y):
        return Int16(self.actual + y.actual)
    
    def __sub__(self, y):
        return Int16(self.actual - y.actual)

    def __mul__(self, y):
        return Int16(self.actual * y.actual)

    def __truediv__(self, y):
        return Int16(self.actual // y.actual)

    def __and__(self, y):
        return Int16(self.actual & y.actual)

    def __or__(self, y):
        return Int16(self.actual | y.actual)

    def __xor__(self, y):
        return Int16(self.actual ^ y.actual)

    def __lshift__(self, y):
        return Int16(self.actual << y.actual)

    def __rshift__(self, y):
        return Int16((self.actual % 0x10000) >> y.actual)

    def __neg__(self):
        return Int16(-self.actual)

    def __invert__(self):
        return Int16(-self.actual - 1)

    def __str__(self):
        hex_s = hex(self.actualValue() & 0xFFFF).split('x')[1].upper()
        return ''.join(['0x']+['0' for _ in range(max(0, 4 - len(hex_s)))]+[hex_s])

    def __repr__(self):
        return self.__str__()