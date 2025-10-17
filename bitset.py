from __future__ import annotations

"""
    This is a basic implementation of bitset.
    It is far more memory efficient than using a Python list,
    which is very useful when dealing with 2^32 bits.
"""

class bitset:
    def __init__(self, n: int):
        self.n = n
        self.A = [0] * ((n // 63) + 1)

    def copy(self) -> bitset:
        out = bitset(0)
        out.n = self.n
        out.A = self.A[:]
        return out
    
    def __eq__(self, other: bitset) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __getitem__(self, i: int) -> int:
        return (self.A[i//63] >> (i % 63)) & 1
    
    def __setitem__(self, i:int, val:int):
        if val:
            self.A[i//63] |= 1 << (i % 63)
        else:
            self.A[i//63] &= ~(1 << (i % 63))
    
    def __len__(self) -> int:
        return self.n

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    
    def sum(self) -> int:
        return sum(x.bit_count() for x in self.A)

    def __or__(self, B: bitset) -> bitset:
        assert self.n == B.n
        C = bitset(self.n)
        data1 = self.A
        data2 = B.A
        data3 = C.A
        for i in range(len(data1)):
            data3[i] = data1[i] | data2[i]
        return C
    
    def __and__(self, B: bitset) -> bitset:
        assert self.n == B.n
        C = bitset(self.n)
        data1 = self.A
        data2 = B.A
        data3 = C.A
        for i in range(len(data1)):
            data3[i] = data1[i] & data2[i]
        return C

    def __xor__(self, B: bitset) -> bitset:
        assert self.n == B.n
        C = bitset(self.n)
        data1 = self.A
        data2 = B.A
        data3 = C.A
        for i in range(len(data1)):
            data3[i] = data1[i] ^ data2[i]
        return C
