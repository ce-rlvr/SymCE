import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False

    # If the witness is provided as a dictionary
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('H1', False))
            h2 = bool(witness.get('H2', False))
            neg_q = bool(witness.get('neg_Q', False))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # If the witness is a tuple (R, S, K, L, f) of custom objects
    try:
        R, S, K, L, f = witness
        try:
            h1 = bool(K.is_field_of_fractions(R) and L.is_field_of_fractions(S))
        except Exception:
            pass
        try:
            h2 = bool(f.is_injective() and f.is_homomorphism(R, S))
        except Exception:
            pass
        try:
            neg_q = not bool(f.extends_uniquely(K, L))
        except Exception:
            pass
        if h1 or h2 or neg_q:
            return [h1, h2, neg_q]
    except Exception:
        pass

    # If the witness is an object with evaluation methods
    try:
        h1 = bool(witness.H1())
    except Exception:
        try:
            h1 = bool(witness.is_field_of_fractions())
        except Exception:
            pass

    try:
        h2 = bool(witness.H2())
    except Exception:
        try:
            h2 = bool(witness.is_injective_homomorphism())
        except Exception:
            pass

    try:
        neg_q = bool(witness.neg_Q())
    except Exception:
        try:
            neg_q = not bool(witness.f_extends_uniquely())
        except Exception:
            pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let K and L be the fields of fractions of R and S, respectively",
    "H_2: Let f: R \\to S be an injective ring homomorphism",
    "¬Q: There does not exist a unique injective ring homomorphism \\tilde{f}: K \\to L such that \\tilde{f}(a/1) = f(a)/1 for all a \\in R"
]

N_HYP = 2
NEG_Q_INDEX = 2