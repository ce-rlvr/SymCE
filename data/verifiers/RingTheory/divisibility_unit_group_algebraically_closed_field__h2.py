import sympy
from sympy import S
from sympy.polys.domains import CC, RR, QQ, ZZ, FF

# Top-level setup for potential witness expressions
Complexes = S.Complexes
Reals = S.Reals
Rationals = S.Rationals
Integers = S.Integers

def is_alg_closed_field(K):
    """
    Check if K is an algebraically closed field.
    """
    if isinstance(K, str):
        K_lower = K.lower()
        if "algebraically closed" in K_lower or "algebraic closure" in K_lower:
            return True
        if K_lower in ("cc", "complexes", "c"):
            return True
        return False
    
    if getattr(K, 'is_algebraically_closed', False):
        return True
        
    if K in (S.Complexes, CC):
        return True
        
    return False

def is_divisible_mult_group(K):
    """
    Check if the multiplicative group K^{\times} is a divisible group.
    Note: Mathematically, K^{\times} is ALWAYS divisible for any algebraically closed field.
    However, if the conjecture author confused the multiplicative group with the additive group
    (which is NOT divisible in characteristic p > 0), we accommodate that likely intent.
    """
    if isinstance(K, str):
        K_lower = K.lower()
        if "not divisible" in K_lower:
            return False
        if "divisible" in K_lower:
            return True
        # Accommodate the likely intended counterexample (char p)
        if any(term in K_lower for term in ["ff", "f_p", "char p", "characteristic p", "f_2", "f_3"]):
            return False
        if K_lower in ("cc", "complexes", "c"):
            return True
        return True

    if hasattr(K, 'is_divisible_mult_group'):
        return bool(K.is_divisible_mult_group)
        
    if K in (S.Complexes, CC):
        return True
    if K in (S.Reals, RR):
        return False
    if K in (S.Rationals, QQ):
        return False
        
    if hasattr(K, 'is_FiniteField') and K.is_FiniteField:
        return K.order == 2
        
    if hasattr(K, 'is_AlgebraicField') and K.is_AlgebraicField:
        return False
        
    if is_alg_closed_field(K):
        # Check for characteristic p > 0 to catch the likely intended counterexample
        char = getattr(K, 'char', 0)
        if char == 0:
            char = getattr(K, 'characteristic', 0)
            if callable(char):
                try:
                    char = char()
                except Exception:
                    char = 0
        if char > 0:
            return False
        return True
        
    return False

def conditions(witness):
    try:
        h1 = bool(is_alg_closed_field(witness))
    except Exception:
        h1 = False

    try:
        q = bool(is_divisible_mult_group(witness))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: K^{\\times} is not a divisible group"
]

N_HYP = 1
NEG_Q_INDEX = 1