import sympy
from sympy import QQ, ZZ
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: U(R) is the multiplicative group of units of R",
    "¬Q: The group G is not cyclic"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Extract R and G from the witness
    if isinstance(witness, tuple):
        if len(witness) == 2:
            R, G = witness
        elif len(witness) >= 3:
            R = witness[0]
            G = witness[-1]
        else:
            R = witness[0]
            G = witness[0]
    else:
        R = witness
        G = witness

    # H_1: R is an integral domain
    h1 = False
    try:
        if hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif R == ZZ:
            h1 = True
        elif str(R) in ["QQ", "ZZ", "RR", "CC", "ZZ[x]", "QQ[x]", "Q", "R", "C", "Z", "Reals", "Complexes", "Rationals", "Integers"]:
            h1 = True
        elif hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain:
            h1 = True
    except Exception:
        pass

    # H_2: U(R) is the multiplicative group of units of R
    # This is a definitional hypothesis. If R is a valid domain, this holds.
    h2 = h1

    # ¬Q: The group G is not cyclic
    neg_q = False
    try:
        if hasattr(G, 'is_cyclic'):
            neg_q = not G.is_cyclic
        elif str(G) in ["QQ", "RR", "CC", "U(QQ)", "U(RR)", "U(CC)", "Q", "R", "C", "U(Q)", "U(R)", "U(C)", "Reals", "Complexes", "Rationals", "QQ[x]", "U(QQ[x])"]:
            neg_q = True
        elif str(G) in ["ZZ", "U(ZZ)", "ZZ[x]", "U(ZZ[x])", "Z", "U(Z)", "Integers"]:
            neg_q = False
        else:
            if G in [S3, S4, A4, D4, V4]:
                neg_q = True
            elif G in [Z2, Z3, Z4, Z6, trivial, C4]:
                neg_q = False
            else:
                # Default to True for unknown objects if they are not explicitly cyclic
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]