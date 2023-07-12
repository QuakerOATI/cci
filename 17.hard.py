

class AddWithoutPlus:
    """Write a function that add two numbers without using any arithmetic operators."""
    _chapter = 17
    _problem_number = 1
    def _add_digits(self, d1, d2):
        res = d1^d2
        if not res == d1|d2:
            # carry
            res |= 1<<1
        return res

    def _add_power_of_two(self, num, power):
        while power:
            digit = num&power
            num ^= power
            if digit:
                num <<= 1
            else:
                power = 0
        return num
        
    def solution(self, first, second):
        pos = 0
        ans = 0
        while first | second:
            d1, d2 = 1&first, 1&second
            ans = self._add_power_of_two(
                    ans,
                    self._add_digits(d1, d2) << pos
                )
            first >>= 1
            second >>= 1
            pos += 1
        return ans
    def test(self):
        pass
            

class Shuffle:
    """Write a function to generate a perfect shuffle (i.e., one in which each
    permutation is equally likely)."""
    import random
    _chapter = 17
    _problem_number = 2
    def solution(self, deck):
        ret = list(deck)
        for j in range(len(ret)):
            k = self.random.randint(j, len(ret)-1)
            ret[j], ret[i] = ret[i], ret[j]
        return ret

class RandomSet:
    """Generate a random subset of an array of m integers of size n, such that
    all such subsets have equal probability of being chosen."""
    _chapter = 17
    _problem_number = 2
    pass

class CountOfTwos:
    """Write a function to count the number of 2s that occur in all the numbers
    n such that 0 <= n <= N."""
    _chapter = 17
    _problem_number = 6
    def __init__(self):
        self._results = {0: 0}

    def _radix_height(self, r, n):
        """Calculates the floor of log_r n."""
        ret = -1
        while n:
            ret += 1
            n //= r
        return n

    def _radix_significand(self, r, n):
        """Calculates the most significant digit of n in base r."""
        ret = 1
        while n > r:
            ret *= r
            n //= r
        return ret*n

    def solution(self, N):
        s = self._radix_significand(10, N)
        pos = 1
        tot = 0
        while s > 10:
            s //= 10
            tot *= 10
            tot += pos
            pos *= 10
        tot *= (s+1)
        if s > 2:
            tot += pos*10
        return tot
    
    def check(self, N):
        try:
            return self._results[N]
        except KeyError:
            last = max(filter(lambda k: k < N, self._results))
            tot = self._results[last]
            for n in range(last+1, N+1):
                tot += str(n).count("2")
                self._results[n] = tot
            return tot


class KthMultiple:
    """Find the kth natural number whose only prime factors are 3, 5, and 7."""
    _chapter = 17
    _problem_number = 9
    class _Node:
        def __init__(self, container, exps, val=None, left=None, right=None, parent=None):
            self._container = container
            self.exps = exps
            self.val = val if val is not None else self._container._getval(exps)
            self.left = left
            self.right = right
        def down(self, val):
            curr, prev = self, self.parent
            while curr.val > val:
                prev = curr
                if curr.left is not None and val < curr.left.val:
                    curr = curr.left
                elif curr.right is not None and val < curr.right.val:
                    curr = curr.right
                else:
                    return curr
            return curr
        def up(self, val):
            curr, prev = self, None
            while curr is not None and curr.val < val:
                prev = curr
                curr = self.parent
            return curr if curr is not None else prev
        def root(self):
            curr = self
            while curr.parent is not None:
                curr = curr.parent
            return curr
        def add_down(self, node):
            parent = self.down(node.val)
            if parent is None:
                node.left = self.left
                node.right = self
                self.parent = node
                self.balance_left()
            else:
                self.left = parent.left
                self.right = parent.right
                parent.right = self
                parent.left = None
                parent.balance_left()
        def balance_left(self):
            if self.left is not None:
                return True
            if self.right is not None:
                if self.right.balance_left():
                    self.left = self.right.left
                    return self.right.balance_left()
            return False
        def is_left_child(self):
            return self.parent is not None and self.parent.left is self
        def succ(self):
            pass


                




    def __init__(self, *primes):
        self._primes = primes
        self._mults = self._Node(1, [0 for p in self._primes])
    def solution(self, *primes):
        """strategy: store the numbers in a self-balancing binary tree"""
        pass
    def _getval(self, exps):
        tot = 1
        exps.reverse()
        for p in self._primes:
            tot *= p**exps.pop()
        return tot


class MajorityElement:
    """Find the majority element in an array of natural numbers, using only O(N)
    time and O(1) space."""
    _chapter = 17
    _problem_number = 10
    pass


from abc import ABC
class SearchTree:

    class _Node:

        def __init__(self, val, left, right):
            self.value = val
            self._weight = 1
            self._left = None
            self._right = None
            self._parent = None
            self.left, self.right = left, right

        @property
        def parent(self):
            return self._parent

        @property
        def weight(self):
            return self._weight

        @property
        def left(self):
            return self._left

        @property
        def right(self):
            return self._left

        @left.setter
        def left(self, child):
            if child is not None:
                self._weight += child.weight
            if self._left is not None:
                self._weight -= self._left.weight
            self._left = child

        @right.setter
        def right(self, child):
            if child is not None:
                self._weight += child.weight
            if self._right is not None:
                self._weight -= self._right.weight
            self._right = child

        def is_left_child(self):
            return self._parent is not None and self._parent.left is self

        def is_right_child(self):
            return self._parent is not None and self._parent.right is self

        @classmethod
        def get_sentinel(cls, val=None, weight=0):
            ret = cls(val, None, None)
            ret._weight = weight
            return ret


    def __init__(self, root_val):
        self._STOP = self._Node.get_sentinel()
        self._root = self._Node(root_val)

    def _walk(self, go_left, go_right):
        curr = self._root
        while True:
            if go_left(curr):
                curr = curr.left
            elif go_right(curr):
                curr = curr.right
            else:
                break
        return curr

    def add(self, val):
        pass
