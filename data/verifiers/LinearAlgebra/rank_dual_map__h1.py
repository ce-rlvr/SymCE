import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import sympy.combinatorics as comb

# Top-level setup: named object bindings
S3 = comb.SymmetricGroup(3)
S4 = comb.SymmetricGroup(4)
A4 = comb.AlternatingGroup(4)
D4 = comb.DihedralGroup(4)
C4 = comb.CyclicGroup(4)
V4 = comb.AlternatingGroup(4)
Z2 = comb.CyclicGroup(2)
Z3 = comb.CyclicGroup(3)
Z4 = comb.CyclicGroup(4)
Z6 = comb.CyclicGroup(6)
trivial = comb.CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    h3_ok = False
    neg_q = False

    try:
        # Witness can be a single matrix T, or a tuple (T, T_star)
        if isinstance(witness, tuple) and len(witness) == 2:
            T, T_star = witness
            if hasattr(T, 'transpose'):
                expected_T_star = T.transpose()
            elif hasattr(T, 'T'):
                expected_T_star = T.T
            else:
                expected_T_star = None
            h3_ok = (T_star == expected_T_star)
        else:
            T = witness
            if hasattr(T, 'transpose'):
                T_star = T.transpose()
            elif hasattr(T, 'T'):
                T_star = T.T
            else:
                T_star = None
            h3_ok = True

        # H1: V and W are finite-dimensional (represented by a finite matrix)
        if hasattr(T, 'shape') and len(T.shape) == 2:
            h1_ok = True
            # H2: T is a linear transformation (a matrix represents a linear map)
            h2_ok = True
        else:
            h1_ok = False
            h2_ok = False

        # H3: T^* is the dual map of T
        if not h1_ok or T_star is None:
            h3_ok = False

    except Exception:
        pass

    try:
        # ¬Q: rank(T) != rank(T^*)
        if h1_ok and h2_ok and h3_ok:
            rank_T = T.rank()
            rank_T_star = T_star.rank()
            neg_q = bool(rank_T != rank_T_star)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are finite-dimensional",
    "H_2: T: V \\to W is a linear transformation",
    "H_3: T^*: W^* \\to V^* is the dual map of T",
    "¬Q: rank(T) != rank(T^*)"
]

N_HYP = 3
NEG_Q_INDEX = 3