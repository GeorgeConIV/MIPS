
class ALU:
    def update(self, a, b, ctrl):
        self.a = a
        self.b = b
        self.ctrl = ctrl

        self.out = [
            lambda x, y : x + y,
            lambda x, y : x - y,
            lambda x, y : x * y,
            lambda x, y : x / y,
            lambda x, y : x & y,
            lambda x, y : x | y,
            lambda x, y : x ^ y,
            lambda x, y : x & ~(y)
        ][ctrl](a, b)

        self.c = True if (self.out & 0x10000) != 0 else False
        self.out = self.out & 0xFFFF
        self.z = True if self.out == 0 else False
        self.v = not self.c
        

