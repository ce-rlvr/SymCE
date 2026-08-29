import sympy
from sympy import Symbol

# Top-level setup for witness expressions
x = Symbol('x')
y = Symbol('y')

def is_prime_in_ring(p, R_str):
    """Check if p is a prime element in the specified ring."""
    try:
        p = sympy.sympify(p)
        if R_str == 'ZZ':
            if not p.is_Integer:
                return False
            return sympy.isprime(p)
        elif R_str == 'ZZ[x]':
            if p.is_Integer:
                return sympy.isprime(p)
            if not p.free_symbols.issubset({x}):
                return False
            from sympy import factor_list
            fac = factor_list(p, domain='ZZ')
            # In ZZ[x], content must be 1 or -1 for a polynomial to be prime
            if abs(fac[0]) != 1:
                return False
            if len(fac[1]) == 1 and fac[1][0][1] == 1:
                return True
            return False
        elif R_str == 'QQ[x]':
            if p.is_Number:
                return False
            if not p.free_symbols.issubset({x}):
                return False
            from sympy import factor_list
            fac = factor_list(p, domain='QQ')
            if len(fac[1]) == 1 and fac[1][0][1] == 1:
                return True
            return False
        elif R_str == 'QQ[x,y]':
            if p.is_Number:
                return False
            if not p.free_symbols.issubset({x, y}):
                return False
            from sympy import factor_list
            fac = factor_list(p, domain='QQ')
            if len(fac[1]) == 1 and fac[1][0][1] == 1:
                return True
            return False
    except Exception:
        return False
    return False

def is_quotient_field(R_str, p):
    """Check if the quotient ring R/(p) is a field."""
    try:
        p = sympy.sympify(p)
        if R_str == 'ZZ':
            if not p.is_Integer:
                return False
            return sympy.isprime(p)
        elif R_str == 'QQ[x]':
            return is_prime_in_ring(p, R_str)
        elif R_str == 'ZZ[x]':
            # No principal ideal in ZZ[x] is maximal
            return False
        elif R_str == 'QQ[x,y]':
            # No principal ideal in QQ[x,y] is maximal
            return False
    except Exception:
        return True
    return True

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    Expected witness format:
    {
        'R': 'ZZ[x]',          # Ring as a string (supported: 'ZZ', 'ZZ[x]', 'QQ[x]', 'QQ[x,y]')
        'p': x,                # Prime element in R
        'M_ideal': [x]         # List of generators for the ideal I, where M = R/I
    }
    """
    try:
        R_str = witness['R']
        p = sympy.sympify(witness['p'])
        I = [sympy.sympify(gen) for gen in witness['M_ideal']]
    except Exception:
        return [False, False, False, False]
    
    # H_1: M is a module over R
    # M = R/I is always a module over R, so we just validate the structure
    try:
        supported_rings = ['ZZ', 'ZZ[x]', 'QQ[x]', 'QQ[x,y]']
        h1 = R_str in supported_rings and isinstance(witness['M_ideal'], list)
    except Exception:
        h1 = False
        
    # H_2: p is a prime element in R
    try:
        h2 = is_prime_in_ring(p, R_str)
    except Exception:
        h2 = False
        
    # H_3: pM = {0}
    # This is satisfied if p is in the ideal I. We check for explicit inclusion.
    try:
        h3 = any(sympy.expand(p - gen) == 0 for gen in I)
    except Exception:
        h3 = False
        
    # ¬Q: M is not a vector space over R/(p)
    # A module is a vector space over R/(p) iff R/(p) is a field.
    # If R/(p) is not a field, M cannot be a vector space (assuming M != {0}).
    try:
        is_field = is_quotient_field(R_str, p)
        m_is_zero = any(sympy.expand(1 - gen) == 0 for gen in I)
        neg_q = (not is_field) and (not m_is_zero)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is a module over R",
    "H_2: p is a prime element in R",
    "H_3: pM = {0}",
    "¬Q: M is not a vector space over R/(p)"
]

N_HYP = 3
NEG_Q_INDEX = 3