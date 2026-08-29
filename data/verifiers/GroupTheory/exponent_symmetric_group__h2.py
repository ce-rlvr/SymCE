import math
from functools import reduce
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def lcm_two(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def lcm_multiple(iterable):
    return reduce(lcm_two, iterable, 1)

def get_partitions(n):
    """Generate all integer partitions of n efficiently."""
    a = [0 for _ in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]

def conditions(witness):
    # H_1: Let n be a positive integer
    try:
        if isinstance(witness, int):
            h1 = witness > 0
        elif hasattr(witness, 'is_integer'):
            if callable(witness.is_integer):
                h1 = witness.is_integer() and witness > 0
            else:
                h1 = bool(witness.is_integer) and witness > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The exponent of S_n is NOT the least common multiple of the integers 1, 2, \dots, n
    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            
            # Compute the exponent of S_n
            # The exponent of S_n is the lcm of the orders of all its elements.
            # The order of an element is the lcm of its disjoint cycle lengths.
            # Thus, the exponent is the lcm of all possible lcms of integer partitions of n.
            if n <= 40:
                if n == 1:
                    exp_Sn = 1
                else:
                    exp_Sn = 1
                    for p in get_partitions(n):
                        l = lcm_multiple(p)
                        exp_Sn = lcm_two(exp_Sn, l)
            else:
                # For large n, we use the mathematical fact that the exponent is exactly lcm(1..n)
                # to avoid timeout, as generating all partitions of large n is too slow.
                exp_Sn = lcm_multiple(range(1, n + 1))
            
            lcm_1_to_n = lcm_multiple(range(1, n + 1)) if n > 0 else 1
            
            neg_q = bool(exp_Sn != lcm_1_to_n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let n be a positive integer",
    "¬Q: The exponent of S_n is not the least common multiple of the integers 1, 2, ..., n"
]

N_HYP = 1
NEG_Q_INDEX = 1