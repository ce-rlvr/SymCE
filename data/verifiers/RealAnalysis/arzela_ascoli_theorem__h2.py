import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Since a true counterexample requires functions taking values in a space where 
    bounded closed sets are not compact (e.g., an infinite-dimensional Banach space),
    which cannot be natively represented as simple SymPy expressions, the witness 
    is expected to be a custom object or dictionary exposing its properties.
    """
    def check(props):
        for p in props:
            if hasattr(witness, p):
                try:
                    v = getattr(witness, p)
                    return bool(v() if callable(v) else v)
                except Exception:
                    pass
            if isinstance(witness, dict) and p in witness:
                try:
                    v = witness[p]
                    return bool(v() if callable(v) else v)
                except Exception:
                    pass
        return False

    try:
        h1 = check(['is_compact', 'X_is_compact', 'compact', 'is_compact_space', 'compact_space'])
    except Exception:
        h1 = False

    try:
        h2 = check(['is_pointwise_bounded', 'pointwise_bounded', 'is_ptwise_bounded'])
    except Exception:
        h2 = False

    try:
        h3 = check(['is_equicontinuous', 'equicontinuous', 'is_equicont'])
    except Exception:
        h3 = False

    try:
        q = check(['has_uniformly_convergent_subsequence', 'uniformly_convergent_subsequence', 
                   'has_convergent_subsequence', 'converges_uniformly', 'has_uniform_subsequence'])
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a compact metric space",
    "H_2: (f_n) is pointwise bounded on X",
    "H_3: (f_n) is an equicontinuous family of functions on X",
    "¬Q: There is no subsequence of (f_n) that converges uniformly on X"
]

N_HYP = 3
NEG_Q_INDEX = 3