import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def _get_bool_attr(w, names, default):
    """Helper to extract boolean properties from mock objects or dicts."""
    if isinstance(w, dict):
        for name in names:
            if name in w:
                val = w[name]
                if callable(val):
                    return bool(val())
                return bool(val)
    else:
        for name in names:
            if hasattr(w, name):
                val = getattr(w, name)
                if callable(val):
                    return bool(val())
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy lacks a comprehensive Galois Theory module for arbitrary rings/fields,
    this verifier uses duck typing to inspect the properties of the witness object.
    """
    # H_1: The extension K/F is finite
    try:
        h1 = _get_bool_attr(witness, ['is_finite', 'finite', 'is_finite_extension'], False)
    except Exception:
        h1 = False

    # H_2: The extension K/F is Galois
    try:
        h2 = _get_bool_attr(witness, ['is_galois', 'galois', 'is_galois_extension'], False)
    except Exception:
        h2 = False

    # neg_Q: The map E \mapsto Gal(K/E) is NOT an inclusion-reversing bijection
    try:
        bijection = _get_bool_attr(witness, [
            'bijection_holds', 
            'bijection', 
            'is_bijection', 
            'has_bijection', 
            'fundamental_theorem_holds'
        ], True)
        neg_q = not bijection
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The extension K/F is finite",
    "H_2: The extension K/F is Galois",
    "¬Q: The map E \\mapsto Gal(K/E) is not an inclusion-reversing bijection between intermediate fields and subgroups of Gal(K/F)"
]

N_HYP = 2
NEG_Q_INDEX = 2