import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture:
    "Every ring is a Dedekind domain" (dropped hypothesis: R is a Euclidean domain).
    
    A counterexample must be a ring that is NOT a Dedekind domain.
    """
    try:
        # Check if witness is a valid ring-like object
        is_valid_ring = getattr(witness, 'is_Ring', False) or witness in (sympy.S.Integers, sympy.S.Rationals)
        if not is_valid_ring:
            return [False]
            
        is_dedekind = False
        
        # Check known Dedekind domains
        if witness in (ZZ, QQ, sympy.S.Integers, sympy.S.Rationals):
            is_dedekind = True
        # Fields are Dedekind domains (Krull dimension 0 or 1 depending on convention, 
        # but Euclidean domains include fields, so they must be included here)
        elif getattr(witness, 'is_Field', False):
            is_dedekind = True
        # Check polynomial rings
        elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            base = witness.domain
            gens = tuple(witness.symbols)
            
            if getattr(base, 'is_Field', False) or base == QQ:
                # K[x_1, ..., x_n] is a Dedekind domain iff n <= 1
                is_dedekind = len(gens) <= 1
            elif base == ZZ:
                # ZZ[x_1, ..., x_n] is a Dedekind domain iff n == 0
                is_dedekind = len(gens) == 0
        # PIDs are Dedekind domains
        elif getattr(witness, 'is_PID', False):
            is_dedekind = True
            
        # The negated conclusion is True if the ring is NOT a Dedekind domain
        neg_q = not is_dedekind
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a Dedekind domain"
]

N_HYP = 0
NEG_Q_INDEX = 0