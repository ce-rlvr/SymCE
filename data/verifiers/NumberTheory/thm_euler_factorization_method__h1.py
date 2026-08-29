import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def conditions(witness):
    n = None
    h1_ok = False
    
    try:
        if isinstance(witness, dict):
            n = int(witness.get('n', 0))
            if all(k in witness for k in ('a', 'b', 'c', 'd')):
                a = int(witness['a'])
                b = int(witness['b'])
                c = int(witness['c'])
                d = int(witness['d'])
                if a > 0 and b > 0 and c > 0 and d > 0:
                    if a**2 + b**2 == n and c**2 + d**2 == n:
                        if set([a, b]) != set([c, d]):
                            h1_ok = True
        elif isinstance(witness, (tuple, list)):
            n = int(witness[0])
            if len(witness) >= 5:
                a = int(witness[1])
                b = int(witness[2])
                c = int(witness[3])
                d = int(witness[4])
                if a > 0 and b > 0 and c > 0 and d > 0:
                    if a**2 + b**2 == n and c**2 + d**2 == n:
                        if set([a, b]) != set([c, d]):
                            h1_ok = True
        else:
            n = int(witness)
    except Exception:
        pass

    if n is None:
        return [False, False]

    try:
        if not h1_ok:
            reps = set()
            limit = math.isqrt(n)
            # Cap the search to prevent timeouts on extremely large n
            if limit > 5 * 10**6:
                limit = 5 * 10**6
            for a in range(1, limit + 1):
                b2 = n - a**2
                if b2 <= 0:
                    continue
                b = math.isqrt(b2)
                if b**2 == b2 and b > 0:
                    reps.add(frozenset([a, b]))
                    if len(reps) >= 2:
                        h1_ok = True
                        break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        # A composite number is a positive integer strictly greater than 1 that is not prime.
        is_composite = (n > 1) and not sympy.isprime(n)
        neg_q_ok = not is_composite
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n can be expressed as the sum of two squares of positive integers in at least two distinct ways",
    "¬Q: The integer n is not a composite number"
]

N_HYP = 1
NEG_Q_INDEX = 1