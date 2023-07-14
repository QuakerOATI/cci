from functools import wraps

class MemoizedFunction(dict):
    def __init__(self, func, seed_memo: dict):
        super().__init__(seed_memo)
        self._function = func
        self._seed = dict(seed_memo)
    def __call__(self, *args, **memo_update):
        for k, v in memo_update.items():
            if k in self:
                self.update((k, v))
        return self._function(*args, **self, **memo_update)
    def reset(self):
        self.clear()
        super().__init__(dict(self._seed))


def memoizer(**kwargs):
    def decorator(fn):
        return wraps(fn)(MemoizedFunction(fn, kwargs))
    return decorator

def memoize(**kwargs):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, show_memo_state=False):
            ret = fn(*args, **kwargs)
            if show_memo_state:
                print(kwargs)
            return ret
        return wrapper
    return decorator

@memoizer(ordered_primes=[2], all_primes={2})
def isprime(n, ordered_primes=[], all_primes=set(), findall_factors=False):
    if n in all_primes and not findall_factors:
        return True
    while ordered_primes[-1]**2 < n:
        last = ordered_primes[-1]
        sieve = [True]*last
        for p in ordered_primes:
            if p*p > 2*last:
                break
            for j in range(last):
                if (last + j + 1) % p == 0:
                    sieve[j] = False
        for j, not_sieved in enumerate(sieve):
            if not_sieved:
                all_primes.add(j + last + 1)
                ordered_primes.append(j + last + 1)
    for p in ordered_primes:
        if p*p > n:
            break
        elif n % p == 0:
            return False
    all_primes.add(n)
    return True

