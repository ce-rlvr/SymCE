import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup for potential witness expressions
Z1 = 1
trivial_ring = 1
Z_1 = 1
trivial = 1

def conditions(witness):
    try:
        # Extract n and R from the witness
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('N', None))
            R = witness.get('R', witness.get('r', None))
        elif isinstance(witness, (tuple, list)):
            if len(witness) >= 2:
                n, R = witness[0], witness[1]
            elif len(witness) == 1:
                n = witness[0]
                R = None
            else:
                n = None
                R = None
        else:
            n = witness
            R = None
            
        # H_1: n is an integer such that n >= 2
        try:
            h1 = int(n) >= 2
        except Exception:
            h1 = False
            
        # ¬Q: The matrix ring M_n(R) IS a Boolean ring.
        # For n >= 2, M_n(R) is a Boolean ring if and only if R is the trivial ring.
        # We check if the provided R represents the trivial ring.
        neg_q = False
        if R is not None:
            try:
                if type(R) in (int, float) and R in [0, 1, -1]:
                    neg_q = True
                elif isinstance(R, sympy.Basic) and R in [sympy.S.Zero, sympy.S.One, sympy.S.NegativeOne]:
                    neg_q = True
                elif hasattr(R, 'zero') and hasattr(R, 'one') and R.zero == R.one:
                    neg_q = True
                elif isinstance(R, (list, set, tuple)) and len(R) == 1:
                    neg_q = True
                elif isinstance(R, str) and any(kw in R.lower() for kw in ["trivial", "zero", "z1"]):
                    neg_q = True
                elif any(kw in str(type(R)).lower() or kw in str(R).lower() for kw in ["trivial", "zero", "z1"]):
                    neg_q = True
            except Exception:
                pass
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "¬Q: The matrix ring M_n(R) is a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1