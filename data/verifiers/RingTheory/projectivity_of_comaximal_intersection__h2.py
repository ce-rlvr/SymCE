import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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

def check_attr(obj, attr_names, default=False):
    """Helper to safely check for attributes or dictionary keys, calling them if they are methods."""
    if isinstance(obj, dict):
        for name in attr_names:
            if name in obj:
                val = obj[name]
                return val() if callable(val) else val
    else:
        for name in attr_names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                return val() if callable(val) else val
    return default

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness should be an object or dictionary with the following properties/keys:
    - is_commutative_ring: True if R is a commutative ring
    - is_comaximal: True if I + J = R
    - I_is_projective: True if I is a projective R-module
    - J_is_projective: True if J is a projective R-module
    - intersection_is_projective: False if I \\cap J is NOT a projective R-module
    """
    try:
        h1 = bool(check_attr(witness, ['is_commutative_ring', 'is_commutative']))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_attr(witness, ['is_comaximal', 'comaximal', 'I_plus_J_eq_R']))
    except Exception:
        h2 = False

    h3 = False
    try:
        i_proj = bool(check_attr(witness, ['I_is_projective', 'I_projective']))
        j_proj = bool(check_attr(witness, ['J_is_projective', 'J_projective']))
        if i_proj and j_proj:
            h3 = True
        elif bool(check_attr(witness, ['are_projective', 'ideals_are_projective'])):
            h3 = True
        else:
            if isinstance(witness, dict) and 'I' in witness and 'J' in witness:
                if bool(check_attr(witness['I'], ['is_projective'])) and bool(check_attr(witness['J'], ['is_projective'])):
                    h3 = True
            elif hasattr(witness, 'I') and hasattr(witness, 'J'):
                if bool(check_attr(witness.I, ['is_projective'])) and bool(check_attr(witness.J, ['is_projective'])):
                    h3 = True
    except Exception:
        h3 = False

    neg_q = False
    try:
        inter_proj = check_attr(witness, ['intersection_is_projective', 'intersection_projective'], default=None)
        if inter_proj is not None:
            neg_q = not bool(inter_proj)
        else:
            if isinstance(witness, dict) and 'intersection' in witness:
                neg_q = not bool(check_attr(witness['intersection'], ['is_projective'], default=True))
            elif hasattr(witness, 'intersection'):
                neg_q = not bool(check_attr(witness.intersection, ['is_projective'], default=True))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal (I + J = R)",
    "H_3: I and J are projective as R-modules",
    "¬Q: The intersection I \\cap J is not a projective R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3