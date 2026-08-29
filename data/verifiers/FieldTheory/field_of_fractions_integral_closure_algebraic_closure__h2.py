import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of sympy domains (R, K).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        R, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is an integral domain
    # In sympy, domains like ZZ, QQ, ZZ[x] represent integral domains.
    try:
        h1 = hasattr(R, 'get_field') and R.get_field() is not None
    except Exception:
        h1 = False
        
    # H_2: K is a field
    try:
        h2 = bool(K.is_Field)
    except Exception:
        h2 = False
        
    # H_3: R is a subring of K
    # We can check this by verifying that unifying K and R yields K.
    try:
        h3 = (K.unify(R) == K)
    except Exception:
        h3 = False
        
    # ¬Q: The field of fractions of S is strictly smaller than the algebraic closure of K.
    # S is the integral closure of R in algebraic_closure(K).
    # The field of fractions of S is the algebraic closure of F (the field of fractions of R).
    # This is exactly algebraic_closure(K) if and only if K is an algebraic extension of F.
    # Thus, the conclusion fails (¬Q is True) iff K is NOT an algebraic extension of F.
    try:
        F = R.get_field()
        if K == F:
            neg_q = False
        elif K == CC and F == RR:
            neg_q = False
        elif K in (RR, CC):
            # RR and CC are transcendental over QQ (and ZZ's fraction field QQ)
            neg_q = True
        elif hasattr(K, 'is_AlgebraicField') and K.is_AlgebraicField:
            # Finite algebraic extensions over QQ
            neg_q = False
        elif hasattr(K, 'is_FiniteField') and K.is_FiniteField and hasattr(F, 'is_FiniteField') and F.is_FiniteField:
            # Finite fields of the same characteristic are algebraic over each other
            neg_q = False
        else:
            # Other fields like QQ(x) are transcendental extensions
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is a field",
    "H_3: R is a subring of K",
    "¬Q: The field of fractions of S is strictly smaller than the algebraic closure of K"
]

N_HYP = 3
NEG_Q_INDEX = 3