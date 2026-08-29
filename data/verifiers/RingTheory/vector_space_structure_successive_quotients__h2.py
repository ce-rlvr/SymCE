import sympy
from sympy import Symbol, Poly, ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, M, n) where:
      - R is a commutative ring (e.g., "ZZ", "QQ[x]", or a SymPy domain)
      - M is a generator for the ideal (e.g., an integer for ZZ, or a polynomial for QQ[x])
      - n is a positive integer
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, M, n = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative ring
    try:
        if isinstance(R, str):
            h1 = R in ["ZZ", "QQ[x]", "ZZ[x]", "RR[x]", "CC[x]"]
        else:
            # SymPy domains and expressions
            h1 = getattr(R, 'is_commutative', True)
    except Exception:
        h1 = False
        
    # H2: n is a positive integer
    try:
        h2 = int(n) == n and n > 0
    except Exception:
        h2 = False
        
    # neg_Q: R/M is not a field (so M^n / M^{n+1} cannot be a vector space over it)
    try:
        is_field = False
        if R == "ZZ" or R == ZZ:
            is_field = sympy.isprime(abs(int(M)))
        elif R == "QQ[x]" or (hasattr(R, 'domain') and R.domain == QQ):
            M_expr = sympy.sympify(M)
            p = Poly(M_expr, x, domain='QQ')
            is_field = p.is_irreducible
        elif R == "ZZ[x]":
            # A principal ideal in ZZ[x] is never maximal
            is_field = False
        else:
            # Fallback for other rings
            if hasattr(M, 'is_prime'):
                is_field = bool(M.is_prime)
            else:
                try:
                    is_field = sympy.isprime(abs(int(M)))
                except Exception:
                    is_field = False
                    
        neg_q = not is_field
    except Exception:
        # If we cannot evaluate the field condition, we fail safely
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a positive integer",
    "¬Q: R/M is not a field (so M^n / M^{n+1} is not a vector space over it)"
]

N_HYP = 2
NEG_Q_INDEX = 2