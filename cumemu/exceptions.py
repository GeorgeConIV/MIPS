class MemoryAccessFault(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

class SyscallInterrupt(Exception):
    pass