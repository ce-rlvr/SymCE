import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import n_order
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
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        a, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a is an integer
    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(p, (int, sympy.Integer))
    except Exception:
        h1 = False
        
    if h1:
        try:
            a = int(a)
            p = int(p)
        except Exception:
            h1 = False

    # H_2: a is a quadratic non-residue modulo p
    try:
        if h1 and p > 0:
            if p > 100000:
                from sympy.ntheory import is_quad_residue
                h2 = not is_quad_residue(a, p)
            else:
                is_res = False
                a_mod = a % p
                for x in range(p):
                    if (x * x) % p == a_mod:
                        is_res = True
                        break
                h2 = not is_res
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The multiplicative order of a modulo p is NOT an even integer
    # (This includes cases where the multiplicative order is undefined, i.e. gcd(a, p) != 1)
    try:
        if h1 and p > 0:
            if math.gcd(a, p) != 1:
                neg_q = True
            else:
                order = n_order(a, p)
                neg_q = (order % 2 != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: a is a quadratic non-residue modulo p",
    "¬Q: The multiplicative order of a modulo p is not an even integer"
]

N_HYP = 2
NEG_Q_INDEX = 2