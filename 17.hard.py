

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

    from random import choice, randint

    def solve(self, arr, n):
        elems = list(arr)
        for i in range(n):
            k = self.randint(i, len(elems)-1)
            elems[i], elems[k] = elems[k], elems[i]
            return elems[:n]

        

    def random_subset(self, arr):
        ret = set()
        for i, item in enumerate(arr):
            if self.choice([True, False]):
                ret.add(item)
        return ret

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
    from math import ceil, sqrt
    from timeit import default_timer as now
    # from .utils.primes import isprime

    def debug(self, msg):
        if self._debug:
            print(msg)

    def __init__(self, primes=[3, 5, 7]):
        self.target_primes = set(primes)
        self.memo = primes
        self._verified = list(primes)
        self.isprime = isprime
        self._debug = False

    def set_debug(self, d):
        self._debug = bool(d)

    def solve(self, k):
        while len(self.memo) < k:
            self.grow_memo()
        return self.memo[k]

    def grow_memo(self):
        self.debug(f"Growing memo.  Original: {self.memo}")
        N = len(self.memo)
        last = self.memo[-1]
        sieve = [False for _ in range(last)]
        self.debug(f"Starting sieve of length {len(sieve)}...")
        for i in range(N):
            if self.memo[i]**2 > 2*last:
                break
            for j in range(i, N):
                num = self.memo[i]*self.memo[j]
                if num > 2*last:
                    break
                elif num <= last:
                    continue
                else:
                    sieve[num - last - 1] = True
        self.debug(f"Done sieving: sieve = {sieve}")
        for i in range(len(sieve)):
            if sieve[i]:
                self.memo.append(i + last + 1)
        self.debug(f"Final memo state after growing: {self.memo}")

    def generate_testcase(self, n):
        while n >= len(self._verified):
            self._grow_verified()
        return (n, self._verified[n])

    def _grow_verified(self):
        last = self._verified[-1]
        for j in range(self._verified[0]*last):
            num = last + j + 1
            if self.isprime(num, findall_factors=True) and num not in self.target_primes:
                continue
            add = True
            for p in self.isprime["ordered_primes"]:
                if num % p == 0 and p not in self.target_primes:
                    add = False
                    break
                # Note: can't do the usual "if p*p > num" thing here
                if p > num/2:
                    break
            if add:
                self._verified.append(num)

    def _grow_verified_simple(self):
        last = self._verified[-1]
        for num in range(last+1, self._verified[0]*last):
            orig = num
            for p in self.target_primes:
                while num % p == 0:
                    num /= p
            if num == 1:
                self._verified.append(orig)



    def test(self, n):
        begin = self.now()
        print("Generating testcase...")
        tc = self.generate_testcase(n)
        testcase_done = self.now()
        print(f"Testcase generated in {testcase_done - begin}s:")
        print(f"    n           = {tc[0]}")
        print(f"    expected    = {tc[1]}")
        print(f"Solving...")
        try:
            ret = self.solve(tc[0])
            if ret != tc[1]:
                print(f"Bummer, dude: ret = {ret}, expected = {tc[1]}")
            else:
                print(f"Test passed!  Hooray for you!")
        except Exception as e:
            print(f"The end-times are upon us, repent while ye may: {e}")
        finally:
            print(f"    solution    -->     {self.now() - testcase_done}s")
            print(f"    total       -->     {self.now() - begin}s")

            


                




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

    from collections import Counter
    from random import randint, choice, shuffle
    from timeit import default_timer as now

    NUM_BITS = 32

    def __init__(self):
        self.tests = {"passed": {}, "failed": {}}
    
    def solve(self, mat):
        counter = self.Counter({(1 << j): 0 for j in range(self.NUM_BITS)})
        for x in mat:
            for p in counter.keys():
                counter[p] += int(x & p != 0)
        return sum([k for k, v in counter.items() if v > len(mat)//2])

    def generate_testcase(self, size=range(5, 5000)):
        if not isinstance(size, int):
            size = self.choice(size)
        maj = self.randint(0, 2**self.NUM_BITS - 1)
        maj_num = self.randint(size//2 + 1, size)
        mat = [maj] * maj_num + [self.randint(0, 2**self.NUM_BITS - 1) for _ in range(size - maj_num)]
        self.shuffle(mat)
        return (mat, maj)

    def gather_testdata(self, size_min=100, size_max=5000, num_trials=100):
        method_start = self.now()
        num_tests_run = 0
        prev_percent = 0
        num_passed, num_failed, num_excs = 0, 0, 0
        for j in range(num_trials):
            percent = 100 * num_tests_run / (num_trials * (size_max - size_min))
            if percent - prev_percent > 10:
                print(f"Progress: {percent}% of tests completed at start of trial {j}...")
                prev_percent = percent
            for size in range(size_min, size_max):
                tc = self.generate_testcase(size=size)
                start = self.now()
                try:
                    ret = self.solve(tc[0])
                    stop = self.now()
                    if ret == tc[1]:
                        self.tests["passed"].setdefault(size, [])
                        self.tests["passed"][size].append(stop - start)
                        num_passed += 1
                    else:
                        self.tests["failed"].append((tc, ret))
                        num_failed += 1
                except Exception as e:
                    self.tests["failed"].append((tc, e))
                    num_excs += 1
                finally:
                    num_tests_run += 1

        done = self.now()
        print(f"Testing finished!")
        print(f"    Time:                   {done - method_start} s")
        print(f"    Number of tests:        {num_tests_run}")
        print(f"    Number of trials:       {num_trials}")
        print(f"    Passed:                 {num_passed} ({100*num_passed/num_tests_run}%)")
        print(f"    Failed:                 {num_failed} ({100*num_failed/num_tests_run}%)")
        print(f"    Exceptions:             {num_excs} ({100*num_excs/num_tests_run}%)")
                    
