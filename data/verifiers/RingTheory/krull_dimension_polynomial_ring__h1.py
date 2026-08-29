import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_bool_attr(obj, *names):
    if isinstance(obj, dict):
        for name in names:
            if name in obj:
                return bool(obj[name])
    else:
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val):
                    return bool(val())
                return bool(val)
    raise AttributeError(f"None of {names} found")

def get_int_attr(obj, *names):
    if isinstance(obj, dict):
        for name in names:
            if name in obj:
                return int(obj[name])
    else:
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val):
                    return int(val())
                return int(val)
    raise AttributeError(f"None of {names} found")

def get_dim_Rx(obj):
    if isinstance(obj, dict):
        for name in ['dim_Rx', 'dim_poly_ring', 'dim_poly', 'dim_R_x']:
            if name in obj:
                return int(obj[name])
    else:
        for name in ['dim_Rx', 'dim_poly_ring', 'dim_poly', 'dim_R_x']:
            if hasattr(obj, name):
                val = getattr(obj, name)
                return int(val()) if callable(val) else int(val)
        if hasattr(obj, 'polynomial_ring'):
            rx = obj.polynomial_ring()
            return get_int_attr(rx, 'dim', 'krull_dimension', 'dim_R')
    raise AttributeError("Cannot find dim(R[x])")

def conditions(witness) -> list[bool]:
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    # Check if witness is a tuple (R, Rx)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, Rx = witness
        try:
            h1 = get_bool_attr(R, 'is_noetherian', 'is_Noetherian', 'noetherian')
        except Exception:
            h1 = False
        try:
            dim_r = get_int_attr(R, 'dim', 'krull_dimension', 'dim_R')
            dim_rx = get_int_attr(Rx, 'dim', 'krull_dimension', 'dim_R')
            neg_q = (dim_rx != dim_r + 1)
        except Exception:
            neg_q = False
        return [h1, neg_q]

    # Otherwise, assume witness is R itself
    try:
        h1 = get_bool_attr(witness, 'is_noetherian', 'is_Noetherian', 'noetherian')
    except Exception:
        h1 = False

    try:
        dim_r = get_int_attr(witness, 'dim', 'krull_dimension', 'dim_R')
        dim_rx = get_dim_Rx(witness)
        neg_q = (dim_rx != dim_r + 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: The Krull dimension of the polynomial ring over R is not equal to dim(R) + 1"
]

N_HYP = 1
NEG_Q_INDEX = 1