import sympy
from sympy import sqrt, Rational, I, pi, cbrt, minimal_polynomial, degree, factor
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

# Top-level setup
# Witnesses are expected to be tuples of SymPy expressions representing 
# the generators of the fields K and L over F=Q.
# Example witness: (cbrt(2), sqrt(2))

def is_algebraic(expr):
    """Check if an expression is algebraic over Q."""
    try:
        poly = minimal_polynomial(expr, x)
        return poly is not None
    except Exception:
        return False

def is_galois_extension(exprs):
    """
    Check if the field extension Q(exprs)/Q is Galois.
    A finite extension is Galois iff the minimal polynomial of each generator
    splits completely into linear factors over the extension field.
    """
    try:
        if len(exprs) == 1:
            elem = exprs[0]
        else:
            elem, _ = primitive_element(exprs, ex=True)
            
        for expr in exprs:
            poly = minimal_polynomial(expr, x)
            # Factor the minimal polynomial over the extension field Q(elem)
            factored = factor(poly, extension=elem)
            
            # Extract the factors
            if factored.is_Mul:
                factors = [arg for arg in factored.args if arg.has(x)]
            elif factored.has(x):
                factors = [factored]
            else:
                factors = []
                
            # Check if all factors containing x are linear
            for fac in factors:
                if fac.is_Pow:
                    base = fac.base
                else:
                    base = fac
                    
                if degree(base, x) != 1:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False, False]
        expr_K, expr_L = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: F is a field (We fix F = Q, which is a field)
    h1 = True
    
    # H_2: K and L are finite field extensions of F
    try:
        h2 = bool(is_algebraic(expr_K) and is_algebraic(expr_L))
    except Exception:
        h2 = False
        
    # H_3: K and L are contained in a common extension field
    # (Algebraic numbers in SymPy are embedded in C, a common extension)
    h3 = True
    
    # H_4: L/F is a Galois extension
    try:
        h4 = bool(is_galois_extension([expr_L]))
    except Exception:
        h4 = False
        
    # ¬Q: KL/F is NOT a Galois extension
    try:
        neg_q = not is_galois_extension([expr_K, expr_L])
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K and L are finite field extensions of F",
    "H_3: K and L are contained in a common extension field",
    "H_4: L/F is a Galois extension",
    "¬Q: KL/F is not a Galois extension"
]

N_HYP = 4
NEG_Q_INDEX = 4