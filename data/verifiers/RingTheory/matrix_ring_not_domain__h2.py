import sympy
from sympy import ZZ, QQ
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_pos_int(n):
    try:
        return int(n) == n and n >= 1
    except Exception:
        return False

def is_integral_domain(R):
    if R in (ZZ, QQ):
        return True
    return getattr(R, 'is_domain', False)

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, n = witness
        else:
            R = ZZ
            n = witness
            
        h1 = is_integral_domain(R) and is_pos_int(n)
    except Exception:
        h1 = False

    # ¬Q: M_n(R) does NOT contain non-zero zero divisors
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, n = witness
        else:
            R = ZZ
            n = witness
            
        if not is_pos_int(n):
            neg_q = False
        else:
            # M_n(R) contains non-zero zero divisors iff n >= 2 or R has zero divisors.
            # The conclusion fails (neg_q is True) iff M_n(R) has NO non-zero zero divisors.
            has_zd = (n >= 2) or not is_integral_domain(R)
            neg_q = not has_zd
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: M_n(R) does not contain non-zero zero divisors"
]

N_HYP = 1
NEG_Q_INDEX = 1