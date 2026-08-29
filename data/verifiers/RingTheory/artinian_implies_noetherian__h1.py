import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_bool_attr(obj, *names, default=None):
    """Helper to extract boolean properties from a witness object or dict."""
    for name in names:
        if isinstance(obj, dict) and name in obj:
            return bool(obj[name])
        if hasattr(obj, name):
            val = getattr(obj, name)
            return bool(val() if callable(val) else val)
    return default

def conditions(witness) -> list[bool]:
    # H_1: R satisfies the descending chain condition on ideals (R is Artinian)
    try:
        h1_ok = get_bool_attr(witness, 'is_artinian', 'is_Artinian')
        if h1_ok is None:
            if isinstance(witness, str):
                w = witness.lower()
                # The classic counterexample is a zero ring on a Prüfer p-group
                h1_ok = "prufer" in w or "prüfer" in w or "z(p^infty)" in w
            elif hasattr(witness, 'gens') and hasattr(witness, 'domain'):
                # For SymPy PolyRings, it is Artinian iff it is a field (0 generators)
                h1_ok = (len(witness.gens) == 0 and getattr(witness.domain, 'is_Field', False))
            else:
                h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: R does NOT satisfy the ascending chain condition on ideals (R is not Noetherian)
    try:
        q_ok = get_bool_attr(witness, 'is_noetherian', 'is_Noetherian')
        if q_ok is None:
            if isinstance(witness, str):
                w = witness.lower()
                if "prufer" in w or "prüfer" in w or "z(p^infty)" in w:
                    q_ok = False
                else:
                    q_ok = True
            elif hasattr(witness, 'gens') and hasattr(witness, 'domain'):
                # SymPy PolyRings over standard domains are Noetherian (Hilbert's Basis Theorem)
                q_ok = True
            else:
                q_ok = True
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R satisfies the descending chain condition on ideals (R is Artinian)",
    "¬Q: R does not satisfy the ascending chain condition on ideals (R is not Noetherian)"
]

N_HYP = 1
NEG_Q_INDEX = 1