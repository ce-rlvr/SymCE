import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "In any compact topological space, the connected component of every point 
    is equal to its quasi-component."
    (The dropped hypothesis is that the space must be Hausdorff).
    """
    # H_1: X is a topological space
    h1 = False
    try:
        for attr in ['is_topological_space', 'is_topology', 'is_space']:
            if hasattr(witness, attr):
                val = getattr(witness, attr)
                h1 = bool(val() if callable(val) else val)
                break
            elif isinstance(witness, dict) and attr in witness:
                val = witness[attr]
                h1 = bool(val() if callable(val) else val)
                break
    except Exception:
        pass

    # H_2: X is compact
    h2 = False
    try:
        for attr in ['is_compact', 'compact']:
            if hasattr(witness, attr):
                val = getattr(witness, attr)
                h2 = bool(val() if callable(val) else val)
                break
            elif isinstance(witness, dict) and attr in witness:
                val = witness[attr]
                h2 = bool(val() if callable(val) else val)
                break
    except Exception:
        pass

    # neg_Q: There exists a point x in X where the connected component of x 
    # is not equal to the quasi-component of x.
    neg_q = False
    try:
        found_neg_q = False
        for attr in ['components_equal_quasi_components', 'components_coincide_with_quasi_components', 'components_eq_quasi_components']:
            if hasattr(witness, attr):
                val = getattr(witness, attr)
                neg_q = not bool(val() if callable(val) else val)
                found_neg_q = True
                break
            elif isinstance(witness, dict) and attr in witness:
                val = witness[attr]
                neg_q = not bool(val() if callable(val) else val)
                found_neg_q = True
                break
        
        if not found_neg_q:
            c = None
            qc = None
            for attr in ['components', 'connected_components']:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    c = val() if callable(val) else val
                    break
                elif isinstance(witness, dict) and attr in witness:
                    val = witness[attr]
                    c = val() if callable(val) else val
                    break
            for attr in ['quasi_components']:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    qc = val() if callable(val) else val
                    break
                elif isinstance(witness, dict) and attr in witness:
                    val = witness[attr]
                    qc = val() if callable(val) else val
                    break
            if c is not None and qc is not None:
                neg_q = (c != qc)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: X is compact",
    "¬Q: There exists a point in X whose connected component is not equal to its quasi-component"
]

N_HYP = 2
NEG_Q_INDEX = 2