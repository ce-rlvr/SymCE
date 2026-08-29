import sympy
from sympy import symbols, Rational, Integer, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: I is an ideal of R",
    "¬Q: The quotient ring R/I is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def _eval_attr(obj, attr_name, *args):
    """Helper to evaluate an attribute whether it is a method or a property."""
    attr = getattr(obj, attr_name)
    if callable(attr):
        return attr(*args)
    return attr

def conditions(witness):
    h1, h2, neg_q = False, False, False

    # Handle dictionary-based mock witnesses
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_euclidean_domain', False))
            h2 = bool(witness.get('is_ideal', False))
            neg_q = not bool(witness.get('is_principal_ideal_ring', True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # Attempt to extract R and I from the witness
    R = None
    I = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
    except Exception:
        pass

    # H_1: R is a Euclidean domain
    try:
        if hasattr(witness, 'is_euclidean_domain'):
            h1 = _eval_attr(witness, 'is_euclidean_domain')
        elif R is not None and hasattr(R, 'is_euclidean_domain'):
            h1 = _eval_attr(R, 'is_euclidean_domain')
        elif R is not None and hasattr(R, 'is_EuclideanDomain'):
            h1 = _eval_attr(R, 'is_EuclideanDomain')
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        if hasattr(witness, 'is_ideal'):
            h2 = _eval_attr(witness, 'is_ideal')
        elif I is not None and hasattr(I, 'is_ideal_of'):
            h2 = _eval_attr(I, 'is_ideal_of', R)
        elif R is not None and hasattr(R, 'is_ideal'):
            h2 = _eval_attr(R, 'is_ideal', I)
    except Exception:
        h2 = False

    # ¬Q: The quotient ring R/I is NOT a principal ideal ring
    try:
        if hasattr(witness, 'quotient_is_principal_ideal_ring'):
            q = _eval_attr(witness, 'quotient_is_principal_ideal_ring')
            neg_q = not q
        elif hasattr(witness, 'is_principal_ideal_ring'):
            q = _eval_attr(witness, 'is_principal_ideal_ring')
            neg_q = not q
        elif R is not None and hasattr(R, 'quotient_is_principal_ideal_ring'):
            q = _eval_attr(R, 'quotient_is_principal_ideal_ring', I)
            neg_q = not q
        elif I is not None and hasattr(I, 'is_principal_ideal_ring_quotient'):
            q = _eval_attr(I, 'is_principal_ideal_ring_quotient')
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]