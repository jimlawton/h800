
class Opcode(object):

    def __init__(self, mnemonic, opcode=0, masked=False):
        self._mnemonic = mnemonic
        self._opcode = opcode                   # Opcode mnemonic string.
        self._masked = masked                   # Masked?
