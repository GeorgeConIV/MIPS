import copy

class Int16:
    def __init__(self, x):
        self.set(x)

    def set(self, x):
        if isinstance(x, Int16):
            self.set(x.actual)
        else:
            self.actual = max(min(x, 0x7FFF), -0x8000)
            self.val = abs(x) & 0x7FFF
            self.n = True if x < 0 else False
            self.z = True if x == 0 else False
            self.c = True if (x & 0x10000) == 0 else False
            self.v = not self.c

    def bytes(self):
        return bytes([self.actual & 0xFF00, self.actual & 0xFF])

    def actualValue(self):
        return self.val * (-1 if self.n else 1)

    def __add__(self, y):
        return Int16(self.actual + y.actual)
    
    def __sub__(self, y):
        return Int16(self.actual - y.actual)

    def __str__(self):
        returnStr = bin(self.val).split('b')[1]

        if len(returnStr) < 16:
            length = 16 - len(returnStr)
            for i in range(0, length):
                returnStr = '0' + returnStr

        elif len(returnStr) > 16:
            length = len(returnStr) - 16
            returnStr = returnStr[length:]

        return returnStr

    # please implement other overloaded operators
    # as well as __str__ (which is python's toString())
    # __str__ should print out a binary representation...
    # consider using bin()