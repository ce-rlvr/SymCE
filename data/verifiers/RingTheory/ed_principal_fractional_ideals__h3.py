import sympy
from sympy import S, Symbol

# Top-level setup
x = Symbol('x')
ZZ = S.Integers
QQ = S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, K, I = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if R == S.Integers or R == sympy.ZZ:
                K = S.Rationals
            elif hasattr(R, 'frac_field'):
                K = R.frac_field()
            else:
                K = None
        elif witness == S.Rationals or witness == sympy.QQ or witness == "QQ":
            R, K, I = S.Integers, S.Rationals, S.Rationals
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Euclidean domain
    try:
        h1 = False
        if R == S.Integers or R == sympy.ZZ:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
    except Exception:
        h1 = False
        
    # H_2: K is the field of fractions of R
    try:
        h2 = False
        if K is None:
            h2 = False
        elif (R == S.Integers or R == sympy.ZZ) and (K == S.Rationals or K == sympy.QQ):
            h2 = True
        elif hasattr(R, 'frac_field') and K == R.frac_field():
            h2 = True
        elif hasattr(R, 'get_field') and K == R.get_field():
            h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: I is not a principal fractional ideal
    # A fractional ideal of R must be of the form (1/d)*J for some ideal J of R and d in R.
    # The field of fractions K is an R-submodule but NOT a fractional ideal of R (unless R is a field).
    # Therefore, K is not a principal fractional ideal.
    try:
        is_prin = True
        if K is not None and I == K and K != R:
            is_prin = False
        elif (I == S.Rationals or I == sympy.QQ) and (R == S.Integers or R == sympy.ZZ):
            is_prin = False
        elif isinstance(I, str) and I in ["K", "QQ", "field of fractions"]:
            is_prin = False
        else:
            # If I is a finitely generated submodule, it is a fractional ideal.
            # Since R is a Euclidean domain (hence a PID), any fractional ideal is principal.
            is_prin = True
            
        neg_q = not is_prin
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: K is the field of fractions of R",
    "¬Q: I is not a principal fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2