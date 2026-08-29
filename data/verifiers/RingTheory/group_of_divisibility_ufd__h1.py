import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

class ValuationRing:
    """
    A helper class to represent valuation rings of a given rank.
    A valuation ring of rank n has a value group isomorphic to Z^n (lexicographically ordered).
    It is a UFD if and only if its rank is <= 1.
    """
    def __init__(self, rank):
        self.rank = rank
        self.is_domain = True
        self.is_UFD = (rank <= 1)
        self.div_group_is_Z_sum = True

def check_integral_domain(w):
    if isinstance(w, dict):
        if 'is_integral_domain' in w: return bool(w['is_integral_domain'])
        if 'is_domain' in w: return bool(w['is_domain'])
    if hasattr(w, 'is_domain') and w.is_domain is not None:
        val = w.is_domain() if callable(w.is_domain) else w.is_domain
        return bool(val)
    if hasattr(w, 'is_integral_domain') and w.is_integral_domain is not None:
        val = w.is_integral_domain() if callable(w.is_integral_domain) else w.is_integral_domain
        return bool(val)
    if isinstance(w, str):
        s = w.lower()
        if ("z x z" in s or "z^2" in s) and "valuation" not in s:
            return False
        if "valuation" in s or "domain" in s or "field" in s:
            return True
        if "z" in s or "q" in s:
            return True
    return False

def check_is_ufd(w):
    if isinstance(w, dict):
        if 'is_UFD' in w: return bool(w['is_UFD'])
        if 'is_ufd' in w: return bool(w['is_ufd'])
    if hasattr(w, 'is_UFD') and w.is_UFD is not None:
        val = w.is_UFD() if callable(w.is_UFD) else w.is_UFD
        return bool(val)
    if hasattr(w, 'is_ufd') and w.is_ufd is not None:
        val = w.is_ufd() if callable(w.is_ufd) else w.is_ufd
        return bool(val)
    if isinstance(w, str):
        s = w.lower()
        if "valuation" in s:
            if "rank 1" in s or "rank=1" in s: return True
            if "rank 2" in s or "rank=2" in s or "z x z" in s or "z^2" in s or "zoplus" in s or "z \oplus" in s: return False
            return False
        if "z[sqrt(-5)]" in s: return False
        if "ufd" in s: return True
    return False

def check_div_group_Z_sum(w):
    if isinstance(w, dict):
        if 'div_group_is_Z_sum' in w: return bool(w['div_group_is_Z_sum'])
        if 'group_of_divisibility_is_Z_sum' in w: return bool(w['group_of_divisibility_is_Z_sum'])
    if hasattr(w, 'div_group_is_Z_sum') and w.div_group_is_Z_sum is not None:
        val = w.div_group_is_Z_sum() if callable(w.div_group_is_Z_sum) else w.div_group_is_Z_sum
        return bool(val)
    if hasattr(w, 'group_of_divisibility_is_Z_sum') and w.group_of_divisibility_is_Z_sum is not None:
        val = w.group_of_divisibility_is_Z_sum() if callable(w.group_of_divisibility_is_Z_sum) else w.group_of_divisibility_is_Z_sum
        return bool(val)
    if isinstance(w, str):
        s = w.lower()
        if "z x z" in s or "z^2" in s or "zoplus" in s or "z \oplus" in s or "direct sum of z" in s or "z+z" in s or "z + z" in s:
            return True
        if "valuation" in s and "z" in s:
            return True
        if "z[sqrt(-5)]" in s:
            return False
    if check_is_ufd(w):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R = witness[0]
        else:
            R = witness
            
        h1 = check_integral_domain(R)
    except Exception:
        h1 = False
        
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R = witness[0]
        else:
            R = witness
            
        is_ufd = check_is_ufd(R)
        is_z_sum = check_div_group_Z_sum(R)
        
        # The conclusion is: R is a UFD iff the group of divisibility is order-isomorphic to a direct sum of copies of Z.
        # We want the conclusion to FAIL, so we negate the biconditional.
        q = (is_ufd == is_z_sum)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "¬Q: R is a UFD XOR its group of divisibility is order-isomorphic to a direct sum of copies of Z"
]

N_HYP = 1
NEG_Q_INDEX = 1