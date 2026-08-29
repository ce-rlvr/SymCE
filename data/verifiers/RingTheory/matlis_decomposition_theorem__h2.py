import sympy
from sympy import S

# Top-level setup for potential witness expressions
ZZ = S.Integers
QQ = S.Rationals

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, E), checks if it is a valid counterexample to the false conjecture.
    The witness should be a tuple of two elements representing the ring R and the R-module E.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, E = witness
        elif isinstance(witness, dict):
            R = witness.get('R')
            E = witness.get('E')
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # Check H_1: R is a commutative Noetherian ring
    try:
        if R in [S.Integers, "ZZ", "Z", S.Rationals, "QQ", "Q", "Z_2", "Z_4", "Z_6", "QQ[x]", "ZZ[x]", "R[x]"]:
            h1 = True
        elif hasattr(R, 'is_commutative') and hasattr(R, 'is_noetherian'):
            h1 = bool(R.is_commutative and R.is_noetherian)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # Check ¬Q: E is NOT isomorphic to a direct sum of indecomposable injective modules.
    # Over a Noetherian ring, arbitrary direct sums of injective modules are injective.
    # Thus, E is a direct sum of injective modules if and only if E is injective.
    # The conclusion fails (¬Q is True) iff E is NOT an injective R-module.
    try:
        is_injective = None
        if R in [S.Integers, "ZZ", "Z"]:
            # Over ZZ, injective modules are exactly the divisible groups.
            if E in [S.Integers, "ZZ", "Z", "Z_2", "Z_4", "Z_6"]:
                is_injective = False
            elif E in [S.Rationals, "QQ", "Q", "QQ/ZZ", "Q/Z"]:
                is_injective = True
        elif R in [S.Rationals, "QQ", "Q"]:
            # Over a field, all modules are injective.
            is_injective = True
            
        if is_injective is None:
            if hasattr(E, 'is_injective'):
                is_injective = bool(E.is_injective)
            else:
                # If we cannot determine injectivity, we cannot verify the counterexample.
                is_injective = True # This makes neg_q = False
        
        neg_q = not is_injective
            
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: E is not isomorphic to a direct sum of indecomposable injective modules of the form E(R/P)"
]

N_HYP = 1
NEG_Q_INDEX = 1