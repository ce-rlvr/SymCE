import sympy
from sympy import Poly, simplify, degree, rem, symbols
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    "H_1: L/K is a finite Galois extension with Galois group G",
    "¬Q: The ring of invariants is not the polynomial ring"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if callable(witness):
            witness = witness()
    except Exception:
        pass

    # Check H_1
    try:
        if hasattr(witness, "is_galois_extension"):
            h1 = bool(witness.is_galois_extension())
        elif hasattr(witness, "H1"):
            h1 = bool(witness.H1())
        elif isinstance(witness, dict):
            if "is_galois_extension" in witness:
                h1 = bool(witness["is_galois_extension"])
            elif "H1" in witness:
                h1 = bool(witness["H1"])
    except Exception:
        pass

    # Check neg_Q
    try:
        if hasattr(witness, "invariants_equal_K_x"):
            neg_q = not bool(witness.invariants_equal_K_x())
        elif hasattr(witness, "neg_Q"):
            neg_q = bool(witness.neg_Q())
        elif isinstance(witness, dict):
            if "invariants_equal_K_x" in witness:
                neg_q = not bool(witness["invariants_equal_K_x"])
            elif "neg_Q" in witness:
                neg_q = bool(witness["neg_Q"])
    except Exception:
        pass

    return [h1, neg_q]