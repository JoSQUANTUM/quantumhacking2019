import numpy as np

class BinarySequenceIter:
    def __init__(self, n):
        self.n = n
        self.value = np.zeros(n)
        self.at_end = False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.at_end:
            raise StopIteration
        prev_value = self.value.copy()
        j = self.n - 1
        while j >= 0 and self.value[j] == 1:
            self.value[j] = 0
            j -= 1
        if j >= 0:
            self.value[j] = 1
        else:
            self.at_end = True
        return prev_value

class CombinationSelectorIter:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.value = np.arange(k)
        self.at_end = False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.value[-1] >= self.n or self.at_end:
            raise StopIteration
        prev_value = np.copy(self.value)
        j = self.k - 1
        while self.value[j] == self.n - 1 - (self.k - 1 - j):
            j -= 1
        if j < 0:
            self.at_end = True
        else:
            self.value[j] += 1
            for l in range(j + 1, self.k):
                self.value[l] = self.value[j] + l - j
        return prev_value
                
                