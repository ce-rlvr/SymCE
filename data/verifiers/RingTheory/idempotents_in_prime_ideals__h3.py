import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, RR, CC
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            e = witness.get('e')
            P = witness.get('P')
        else:
            R, e, P = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring with identity
    try:
        if isinstance(R, int) and R >= 2:
            h1 = True
        elif R in (S.Integers, S.Rationals, S.Reals, S.Complexes, ZZ, QQ, RR, CC):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative and hasattr(R, 'has_Identity') and R.has_Identity:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: e is an element of R such that e^2 = e
    try:
        if isinstance(R, int) and R >= 2:
            e_val = int(e)
            h2 = (0 <= e_val < R) and ((e_val * e_val) % R == e_val) and (e == e_val)
        elif R in (S.Integers, S.Rationals, S.Reals, S.Complexes, ZZ, QQ, RR, CC):
            h2 = (e in R) and (e * e == e)
        else:
            h2 = (e * e == e)
    except Exception:
        h2 = False

    # Negated Conclusion: It is not the case that exactly one of e or 1 - e belongs to P
    try:
        if isinstance(R, int) and R >= 2:
            e_val = int(e)
            one_minus_e = (1 - e_val) % R
        else:
            one_minus_e = 1 - e
        
        try:
            in_P_e = bool(e in P)
        except (TypeError, ValueError):
            in_P_e = bool(P(e))
            
        try:
            in_P_1_minus_e = bool(one_minus_e in P)
        except (TypeError, ValueError):
            in_P_1_minus_e = bool(P(one_minus_e))
            
        neg_q = not (in_P_e ^ in_P_1_minus_e)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: e is an element of R such that e^2 = e",
    "¬Q: It is not the case that exactly one of e or 1 - e belongs to P"
]

N_HYP = 2
NEG_Q_INDEX = 2