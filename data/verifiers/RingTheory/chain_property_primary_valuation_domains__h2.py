import sympy
from sympy import *
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
Z = sympy.S.Integers
Q = sympy.S.Rationals
R_real = sympy.S.Reals
C_complex = sympy.S.Complexes

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the conjecture.
    """
    h1_ok = False
    neg_q_ok = False
    
    # The witness might be just the ring R, or a tuple like (R, P) or (R, P, ideals)
    R = witness
    if isinstance(witness, tuple) and len(witness) >= 1:
        R = witness[0]

    # Check H_1: R is a commutative valuation domain
    try:
        if isinstance(R, dict):
            is_comm = R.get('is_commutative', True)
            is_val = R.get('is_valuation_domain', False)
            h1_ok = bool(is_comm) and bool(is_val)
            if 'is_commutative_valuation_domain' in R:
                h1_ok = bool(R['is_commutative_valuation_domain'])
        else:
            if hasattr(R, 'is_commutative_valuation_domain'):
                val = getattr(R, 'is_commutative_valuation_domain')
                h1_ok = bool(val() if callable(val) else val)
            else:
                is_comm = True
                if hasattr(R, 'is_commutative'):
                    val = getattr(R, 'is_commutative')
                    is_comm = bool(val() if callable(val) else val)
                
                is_val = False
                if hasattr(R, 'is_valuation_domain'):
                    val = getattr(R, 'is_valuation_domain')
                    is_val = bool(val() if callable(val) else val)
                
                h1_ok = is_comm and is_val
    except Exception:
        h1_ok = False

    # Check ¬Q: The set of all P-primary ideals in R is NOT totally ordered under inclusion
    try:
        if isinstance(R, dict):
            if 'p_primary_ideals_totally_ordered' in R:
                neg_q_ok = not bool(R['p_primary_ideals_totally_ordered'])
            elif 'primary_ideals_totally_ordered' in R:
                neg_q_ok = not bool(R['primary_ideals_totally_ordered'])
        else:
            if hasattr(R, 'p_primary_ideals_totally_ordered'):
                val = getattr(R, 'p_primary_ideals_totally_ordered')
                neg_q_ok = not bool(val() if callable(val) else val)
            elif hasattr(R, 'primary_ideals_totally_ordered'):
                val = getattr(R, 'primary_ideals_totally_ordered')
                neg_q_ok = not bool(val() if callable(val) else val)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative valuation domain",
    "¬Q: The set of all P-primary ideals in R is not totally ordered under inclusion"
]

N_HYP = 1
NEG_Q_INDEX = 1