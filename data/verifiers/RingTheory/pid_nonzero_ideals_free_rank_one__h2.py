import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for witness expressions
# R can be ZZ, QQ, or other PID domains from sympy.

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    The witness should be a tuple (R, I_gens) where:
      - R is a SymPy domain (e.g., ZZ, QQ)
      - I_gens is an iterable of elements in R generating the ideal I
    """
    try:
        R, I_gens = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a principal ideal domain
    try:
        h1 = bool(getattr(R, 'is_PID', False))
        if h1:
            # Verify that I_gens is an iterable of elements in R
            iter(I_gens)
            for g in I_gens:
                if g not in R:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # ¬Q: I is not a free R-module of rank 1
    try:
        # In a PID, an ideal is a free module of rank 1 if and only if it is non-zero.
        # The conclusion fails (neg_Q is True) if I is NOT a free R-module of rank 1,
        # which means I must be the zero ideal (all generators are zero).
        is_zero = True
        for g in I_gens:
            if g != 0:
                is_zero = False
                break
        neg_q = is_zero
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: I is not a free R-module of rank 1 (i.e., I is the zero ideal)"
]

N_HYP = 1
NEG_Q_INDEX = 1