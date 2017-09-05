from SegmentTree import SegmentTree


class ArraySegmentTreeImpl(SegmentTree):
    _nil = object()

    def __init__(self, aggregation_func):
        self._degree = 0
        self._length = 0
        self._arr = None
        self._aggr = aggregation_func

    def build(self, iterable):
        input = list(iterable)
        if not input:
            raise ValueError("Can not build with empty list")
        self._length = len(input)
        i = 1
        while self._length > i:
            i *= 2
        self._degree = i
        self._arr = [self._nil] * (2 * self._degree - 1)
        self._arr[self._degree:self._degree + self._length] = input
        low = self._degree
        high = self.size + self._length
        while low != 0:
            for x in range(low, high):
                if x % 2 == 0:
                    self._arr[x // 2 - 1] = self._aggr(self._arr[x - 1], self._arr[x])
                elif x == high - 1:
                    self._arr[x // 2] = self._arr[x]
            low = low // 2
            high = (high + 1) // 2 - 1

    def query(self, low, high):
        if not self._arr:
            raise ValueError("Tree not yet built")
        if low >= self._length or high < 0:
            raise IndexError("No value hit by given range")
        return self._query(0, self._degree + low - 1, self._degree + high - 1, self._degree)

    def _query(self, pos, low, high, degree):
        if self._arr[pos] is self._nil:
            return self._nil
        if degree == 1:
            return self._arr[pos]
        left = (pos + 1) * degree - 1
        mid = left + degree // 2 - 1
        right = left + degree - 1
        if low > mid:
            return self._query(pos * 2 + 2, low, high, degree // 2)
        elif high <= mid:
            return self._query(pos * 2 + 1, low, high, degree // 2)
        elif low <= left and high >= right:
            return self._arr[pos]
        else:
            la = self._query(pos * 2 + 1, low, high, degree // 2)
            ra = self._query(pos * 2 + 2, low, high, degree // 2)
            if ra is self._nil:
                return la
            else:
                return self._aggr(la, ra)

    def get(self, idx):
        if not self._arr:
            raise ValueError("Tree not yet built")
        if idx >= self._length or idx < 0:
            raise IndexError("Index out of range")
        return self._arr[self._degree + idx - 1]

    def update(self, idx, val):
        if not self._arr:
            raise ValueError("Tree not yet built")
        if idx >= self._length or idx < 0:
            raise IndexError("Index out of range")
        self._update(idx, val)

    def _update(self, idx, val):
        pos = self._degree + idx - 1
        self._arr[pos] = val
        while True:
            pos = (pos + 1) // 2 - 1
            la = self._arr[pos * 2 + 1]
            ra = self._arr[pos * 2 + 2]
            if ra is self._nil:
                self._arr[pos] = la
            else:
                self._arr[pos] = self._aggr(la, ra)
            if pos == 0:
                break

    def append(self, val):
        if not self._arr:
            self.build([val])
        if self._length == self._degree:
            self._degree *= 2
            new_arr = [self._nil] * (2 * self._degree - 1)
            degree = 1
            new_arr[0] = self._arr[0]
            while degree < self._degree:
                pos = degree - 1
                nex_pos = pos * 2 + 1
                new_arr[nex_pos:nex_pos + degree] = self._arr[pos:pos + degree]
                degree *= 2
        self._length += 1
        self._update(self._length, val)
