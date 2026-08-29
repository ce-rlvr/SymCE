import sympy
from sympy import S

# Top-level setup
CC = sympy.CC
RR = sympy.RR
QQ = sympy.QQ
ZZ = sympy.ZZ
Complexes = S.Complexes
Reals = S.Reals
Rationals = S.Rationals
Integers = S.Integers

def conditions(witness):
    try:
        # The hypothesis "Let R be the field of real numbers" is a context statement.
        # It places no constraints on the witness C.
        h1 = True
    except Exception:
        h1 = False

    try:
        # The algebraic closure of the real numbers is the complex numbers.
        # We check if the witness is the complex field/domain.
        is_alg_closure = (witness == sympy.CC or witness == sympy.S.Complexes)
        neg_q = not is_alg_closure
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let R be the field of real numbers",
    "¬Q: C is not the algebraic closure of R"
]

N_HYP = 1
NEG_Q_INDEX = 1