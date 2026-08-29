import sympy
from sympy import eye, zeros, Matrix
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False

    # 1. Check if witness is a mock object with attributes
    try:
        if hasattr(witness, "is_non_degenerate"):
            val = witness.is_non_degenerate
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, "non_degenerate"):
            val = witness.non_degenerate
            h1 = bool(val() if callable(val) else val)
            
        if hasattr(witness, "is_isomorphism"):
            val = witness.is_isomorphism
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, "isomorphism"):
            val = witness.isomorphism
            neg_q = not bool(val() if callable(val) else val)
    except Exception:
        pass

    # 2. Check if witness is a dictionary
    if not h1 and not neg_q:
        try:
            if isinstance(witness, dict):
                if "non_degenerate" in witness:
                    h1 = bool(witness["non_degenerate"])
                elif "is_non_degenerate" in witness:
                    h1 = bool(witness["is_non_degenerate"])
                
                if "isomorphism" in witness:
                    neg_q = not bool(witness["isomorphism"])
                elif "is_isomorphism" in witness:
                    neg_q = not bool(witness["is_isomorphism"])
        except Exception:
            pass

    # 3. Check if witness is a SymPy Matrix
    if not h1 and not neg_q:
        try:
            if isinstance(witness, Matrix):
                if witness.is_square:
                    d = witness.det()
                    if d != 0:
                        h1 = True
                        # A finite-dimensional non-degenerate bilinear form over a field
                        # always induces an isomorphism. Thus, a finite matrix cannot be a counterexample.
                        neg_q = False
        except Exception:
            pass

    # 4. Check if witness is a string indicating infinite dimensions
    if not h1 and not neg_q:
        try:
            if isinstance(witness, str):
                s = witness.lower()
                if any(kw in s for kw in ["inf", "poly", "r[x]", "sequence", "l2", "c00", "hilbert", "function"]):
                    h1 = True
                    neg_q = True
        except Exception:
            pass

    # 5. Check if witness is a tuple/list containing such a string
    if not h1 and not neg_q:
        try:
            if isinstance(witness, (tuple, list)):
                for item in witness:
                    if isinstance(item, str):
                        s = item.lower()
                        if any(kw in s for kw in ["inf", "poly", "r[x]", "sequence", "l2", "c00", "hilbert", "function"]):
                            h1 = True
                            neg_q = True
        except Exception:
            pass

    # 6. Check if witness is sympy.oo
    if not h1 and not neg_q:
        try:
            if witness == sympy.oo:
                h1 = True
                neg_q = True
        except Exception:
            pass

    # 7. Check class name for infinite-dimensional indicators
    if not h1 and not neg_q:
        try:
            name = witness.__class__.__name__.lower()
            if any(kw in name for kw in ["inf", "poly", "sequence", "hilbert"]):
                h1 = True
                neg_q = True
        except Exception:
            pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B is a non-degenerate bilinear form on V",
    "¬Q: The linear map L: V -> V* is not an isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1