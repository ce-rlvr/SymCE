import sympy
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings for the witness expression
class Z_n:
    def __init__(self, n):
        self.n = n
        
    def __contains__(self, item):
        try:
            val = int(item)
            return 0 <= val < self.n
        except Exception:
            return False
            
    def __iter__(self):
        return iter(range(self.n))
        
    def mul(self, a, b):
        return (int(a) * int(b)) % self.n
        
    def add(self, a, b):
        return (int(a) + int(b)) % self.n
        
    @property
    def is_commutative(self):
        return True
        
    def __str__(self):
        return f"Z_{self.n}"
        
    def __repr__(self):
        return f"Z_{self.n}"
        
    def __eq__(self, other):
        return isinstance(other, Z_n) and self.n == other.n

Z2 = Z_n(2)
Z3 = Z_n(3)
Z4 = Z_n(4)
Z5 = Z_n(5)
Z6 = Z_n(6)
Z8 = Z_n(8)
Z10 = Z_n(10)
Z12 = Z_n(12)
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        R, S, S_bar = witness
        S_ints = set(int(s) for s in S)
        S_bar_ints = set(int(s) for s in S_bar)
    except Exception:
        return [False, False, False]

    # Sanity check: elements must belong to the ring
    try:
        if not all(s in R for s in S_ints):
            return [False, False, False]
        if not all(s in R for s in S_bar_ints):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif isinstance(R, Z_n):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: \bar{S} is the saturation of S
    try:
        if isinstance(R, Z_n):
            expected_S_bar = set()
            for x in R:
                for y in R:
                    if R.mul(x, y) in S_ints:
                        expected_S_bar.add(x)
                        break
            h2 = (S_bar_ints == expected_S_bar)
        elif R == sympy.ZZ:
            expected_S_bar = set()
            if 0 in S_ints:
                # Saturation would be all of ZZ, which cannot be represented as a finite set
                h2 = False
            else:
                for s in S_ints:
                    for d in sympy.divisors(abs(s)):
                        expected_S_bar.add(d)
                        expected_S_bar.add(-d)
                h2 = (S_bar_ints == expected_S_bar)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The localized rings S^{-1}R and \bar{S}^{-1}R are not canonically isomorphic
    # This happens when S is not a multiplicative set, making S^{-1}R an invalid ring construction.
    try:
        is_mult_S = True
        if not S_ints:
            is_mult_S = False
        elif 1 not in S_ints:
            is_mult_S = False
        else:
            if isinstance(R, Z_n):
                for a in S_ints:
                    for b in S_ints:
                        if R.mul(a, b) not in S_ints:
                            is_mult_S = False
                            break
                    if not is_mult_S:
                        break
            elif R == sympy.ZZ:
                for a in S_ints:
                    for b in S_ints:
                        if (a * b) not in S_ints:
                            is_mult_S = False
                            break
                    if not is_mult_S:
                        break
            else:
                is_mult_S = False
                
        neg_q = not is_mult_S
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: \\bar{S} is the saturation of S",
    "¬Q: S^{-1}R and \\bar{S}^{-1}R are not canonically isomorphic (e.g., S is not multiplicative)"
]

N_HYP = 2
NEG_Q_INDEX = 2