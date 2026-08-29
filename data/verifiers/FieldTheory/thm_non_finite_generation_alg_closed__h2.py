import sympy
from sympy import CC, RR, QQ, ZZ

# Top-level setup for Field Theory
# We provide standard sympy domains that might be used as witnesses.

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: K is finitely generated as a field extension over P"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_field_name(F):
    """Helper to normalize field representations to standard string names."""
    if F is None: 
        return ""
    s = str(F).upper()
    if 'C' in s and 'COMPLEX' in s: return 'C'
    if s in ['C', 'CC', 'COMPLEXES']: return 'C'
    if 'R' in s and 'REAL' in s: return 'R'
    if s in ['R', 'RR', 'REALS']: return 'R'
    if 'Q' in s and 'RATIONAL' in s: return 'Q'
    if s in ['Q', 'QQ', 'RATIONALS']: return 'Q'
    return s

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (K, P) or a dict {'K': K, 'P': P}
    representing the field K and the base field P.
    """
    try:
        # Extract K and P from the witness
        if isinstance(witness, dict):
            K = witness.get('K', None)
            P = witness.get('P', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            K, P = witness
        else:
            K = witness
            P = None
            
        # H_1: K is an algebraically closed field
        h1_ok = False
        K_name = get_field_name(K)
        if K_name == 'C' or K_name in ['Q_BAR', 'FP_BAR', 'ALGEBRAIC_CLOSURE']:
            h1_ok = True
        elif hasattr(K, 'is_AlgebraicallyClosed') and K.is_AlgebraicallyClosed:
            h1_ok = True
            
        # ¬Q: K IS finitely generated as a field extension over P
        neg_q_ok = False
        if K is not None and P is not None:
            P_name = get_field_name(P)
            # C is finitely generated over R (degree 2) and over C (degree 1)
            if K_name == 'C' and P_name in ['R', 'C']:
                neg_q_ok = True
            # Any field is finitely generated over itself (degree 1)
            elif K_name == P_name and K_name != "":
                neg_q_ok = True
                
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]