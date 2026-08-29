import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: Let H be the ring of Hurwitz quaternions (witness is a valid quaternion)",
    "¬Q: The equivalence between u being a unit in H and N(u)=1 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_abcd(u):
    if hasattr(u, 'a') and hasattr(u, 'b') and hasattr(u, 'c') and hasattr(u, 'd'):
        return [sympy.S(u.a), sympy.S(u.b), sympy.S(u.c), sympy.S(u.d)]
    elif isinstance(u, (list, tuple)) and len(u) == 4:
        return [sympy.S(x) for x in u]
    else:
        raise ValueError("Not a quaternion")

def conditions(witness):
    try:
        abcd = get_abcd(witness)
        if not all(x.is_real for x in abcd):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    try:
        abcd = get_abcd(witness)
        a, b, c, d = abcd
        norm = a**2 + b**2 + c**2 + d**2
        
        all_int = all(x.is_integer for x in abcd)
        all_half = all((x - sympy.Rational(1, 2)).is_integer for x in abcd)
        in_h = all_int or all_half
        
        # u is a unit in H if and only if it is in H and its norm is 1
        is_unit = in_h and (norm == 1)
        
        # The conclusion states that u is a unit iff its norm is 1.
        # (The second part of the conclusion regarding the group of units of H is a true constant fact).
        conclusion = (is_unit == (norm == 1))
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]