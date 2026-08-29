import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ

# Top-level setup for witness expressions
x, y, z, t = symbols('x y z t')

def is_prime_in_R(p, R):
    from sympy import sympify, factor_list, factorint
    if p == 0:
        return False
    
    try:
        p_expr = sympify(p)
    except Exception:
        return False
    
    if R == ZZ:
        from sympy import isprime
        try:
            return isprime(abs(int(p_expr)))
        except Exception:
            return False
            
    if hasattr(R, 'domain') and hasattr(R, 'gens'):
        base = R.domain
        
        try:
            # Check if p is actually an element of R
            p_R = R.from_sympy(p_expr)
        except Exception:
            return False
            
        try:
            coeff, factors = factor_list(p_expr)
        except Exception:
            return False
            
        if base == ZZ:
            if not coeff.is_Integer:
                return False
            c_factors = factorint(abs(int(coeff)))
            total_prime_factors = sum(c_factors.values()) + sum(mult for f, mult in factors)
            return total_prime_factors == 1
            
        elif hasattr(base, 'is_Field') and base.is_Field:
            total_prime_factors = sum(mult for f, mult in factors)
            return total_prime_factors == 1
            
    return False

def is_field_quotient(p, R):
    from sympy import sympify
    try:
        p_expr = sympify(p)
    except Exception:
        return False
        
    if p_expr == 0:
        if R == ZZ: 
            return False
        if hasattr(R, 'is_Field') and R.is_Field: 
            return True
        if hasattr(R, 'domain') and hasattr(R, 'gens'):
            return False
        return False

    if not is_prime_in_R(p, R):
        return False
        
    if R == ZZ:
        return True
        
    if hasattr(R, 'domain') and hasattr(R, 'gens'):
        base = R.domain
        gens = R.gens
        
        # Krull dimension must be 1 for the quotient by a principal prime ideal to be a field
        if hasattr(base, 'is_Field') and base.is_Field and len(gens) == 1:
            return True
            
        return False
        
    return False

def conditions(witness):
    try:
        R, p = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(is_prime_in_R(p, R))
    except Exception:
        h1 = False
        
    try:
        q = bool(is_field_quotient(p, R))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a non-zero prime element of R",
    "¬Q: The quotient ring R/(p) is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1