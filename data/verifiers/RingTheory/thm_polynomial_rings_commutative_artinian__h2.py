import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _get_bool_prop(obj, prop_names, default=False):
    if isinstance(obj, dict):
        for prop in prop_names:
            if prop in obj:
                return bool(obj[prop])
    for prop in prop_names:
        if hasattr(obj, prop):
            val = getattr(obj, prop)
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
            else:
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative Artinian ring
    try:
        is_comm = _get_bool_prop(witness, ['is_commutative'])
        is_art = _get_bool_prop(witness, ['is_artinian'])
        h1 = is_comm and is_art
    except Exception:
        h1 = False

    # not Q: The polynomial ring over R is NOT a Noetherian ring
    try:
        if isinstance(witness, dict) and 'polynomial_ring_is_noetherian' in witness:
            is_noeth = bool(witness['polynomial_ring_is_noetherian'])
        elif hasattr(witness, 'polynomial_ring_is_noetherian'):
            val = witness.polynomial_ring_is_noetherian
            is_noeth = bool(val() if callable(val) else val)
        else:
            # A polynomial ring over R is Noetherian if and only if R is Noetherian.
            # If the witness doesn't explicitly specify the polynomial ring's property,
            # we check if R itself is Noetherian.
            is_noeth = _get_bool_prop(witness, ['is_noetherian'], default=True)
        neg_q = not is_noeth
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Artinian ring",
    "not Q: The polynomial ring over R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1