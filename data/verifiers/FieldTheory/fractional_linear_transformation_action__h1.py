import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains.domain import Domain

# Top-level setup
Z = ZZ
Q = QQ
R = RR
C = CC

def conditions(witness):
    try:
        # H1: L = K(x) is the field of rational functions in one variable over K.
        # This implies K is an integral domain. In SymPy, this corresponds to a Domain object.
        h1 = isinstance(witness, Domain)
    except Exception:
        h1 = False

    try:
        # ¬Q: The group of K-automorphisms of L is NOT isomorphic to PGL_2(K).
        # If K is an integral domain but not a field (e.g., K = Z), the K-automorphisms
        # of K(x) are the F-automorphisms of F(x) where F is the field of fractions of K.
        # The automorphism group is PGL_2(F), which is strictly larger than PGL_2(K),
        # and the transformations do not necessarily have coefficients in K.
        neg_q = not witness.is_Field
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L = K(x) is the field of rational functions in one variable over K",
    "¬Q: The group of K-automorphisms of L is not isomorphic to PGL_2(K) or does not act by fractional linear transformations over K"
]

N_HYP = 1
NEG_Q_INDEX = 1