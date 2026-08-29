import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Let K be a field.",
    "H_2: Let V be a vector space over K.",
    "H_3: Let \\bigwedge V be the exterior algebra of V.",
    "¬Q: The element \\omega is a unit in \\bigwedge V if and only if \\omega_0 is non-zero is FALSE."
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_flag(witness, *names):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return bool(witness[name])
    else:
        for name in names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                if callable(val):
                    return bool(val())
                return bool(val)
    raise ValueError(f"Missing one of {names}")

def conditions(witness):
    try:
        h1 = get_flag(witness, "K_is_field", "is_field")
    except Exception:
        h1 = False

    try:
        h2 = get_flag(witness, "V_is_vector_space", "is_vector_space")
    except Exception:
        h2 = False

    try:
        h3 = get_flag(witness, "is_exterior_algebra", "exterior_algebra")
    except Exception:
        h3 = False

    try:
        omega_is_unit = get_flag(witness, "omega_is_unit", "is_unit")
        omega_0_is_nonzero = get_flag(witness, "omega_0_is_nonzero", "omega_0_nonzero", "omega_0_neq_0")
        neg_q = not (omega_is_unit == omega_0_is_nonzero)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]