class Stack:
    //test
    def __init__(self, max_size):
        self.max_size = max_size  # public attr
        self._num = 0  # private attr
        self.s = [None] * max_size

    def is_full(self):
        return self._num >= self.max_size

    def is_empty(self):
        return self._num <= 0

    def top(self):
        if self.is_empty():
            raise Exception("Stack empty")
        return self.s[self._num-1]

    def size(self):
        return self._num

    def push(self, x):
        if self.is_full():
            raise Exception("Stack Overflow")
        self.s[self._num] = x
        self._num += 1

    def pop(self):
        if self.is_empty():
            raise Exception("Stack empty")
        self._num -= 1
        return self.s[self._num]

    def peek(self):
        if self.is_empty():
            raise Exception("Stack empty")
        temp = self._num-1
        return self.s[temp]
