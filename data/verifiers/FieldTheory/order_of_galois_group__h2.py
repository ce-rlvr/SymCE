import sympy
import sympy.combinatorics
import sympy.matrices
import math

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    h1, h2, neg_q = False, False, False
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_extension", False))
            h2 = bool(witness.get("is_galois", False))
            deg = witness.get("degree", None)
            order = witness.get("galois_group_order", None)
            if deg is not None and order is not None:
                neg_q = (deg != order)
        else:
            h1 = bool(getattr(witness, "is_extension", False))
            h2 = bool(getattr(witness, "is_galois", False))
            deg = getattr(witness, "degree", None)
            order = getattr(witness, "galois_group_order", None)
            if deg is not None and order is not None:
                neg_q = (deg != order)
    except Exception:
        pass
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field extension of F",
    "H_2: The extension K over F is Galois",
    "¬Q: The order of the Galois group is not equal to the degree of the extension"
]

N_HYP = 2
NEG_Q_INDEX = 2