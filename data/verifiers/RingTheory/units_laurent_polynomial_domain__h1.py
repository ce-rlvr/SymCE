import sympy
from sympy.abc import x
from sympy.ntheory import factorint
from math import gcd

def get_laurent_terms(expr, x_sym, n):
    expr = sympy.expand(expr)
    if expr == 0:
        return {}
    
    terms = {}
    args = expr.args if expr.is_Add else [expr]
    for arg in args:
        c, e = arg.as_coeff_exponent(x_sym)
        if not getattr(c, 'is_integer', False):
            raise ValueError("Coefficient not an integer")
        if not getattr(e, 'is_integer', False):
            raise ValueError("Exponent not an integer")
            
        try:
            e_int = int(e)
            c_int = int(c)
        except TypeError:
            raise ValueError("Not concrete numbers")
            
        c_int = c_int % n
        if c_int != 0:
            terms[e_int] = terms.get(e_int, 0) + c_int
            
    terms = {e: c % n for e, c in terms.items() if c % n != 0}
    return terms

def is_unit_laurent(terms, n):
    # A Laurent polynomial over Z/nZ is a unit iff for every prime factor p of n,
    # its reduction modulo p has exactly one non-zero term.
    factors = factorint(n)
    for p in factors:
        non_zero_count = sum(1 for c in terms.values() if c % p != 0)
        if non_zero_count != 1:
            return False
    return True

def is_form_axk(terms, n):
    if len(terms) != 1:
        return False
    c = list(terms.values())[0]
    return gcd(c, n) == 1

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple (n, u_expr) where:
      - n is an integer >= 2 (representing the ring R = Z/nZ)
      - u_expr is a SymPy expression representing a Laurent polynomial in x over Z/nZ
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        n, u_expr = witness
        
        # H_1: R is a valid ring (we use Z/nZ)
        h1 = isinstance(n, int) and not isinstance(n, bool) and n >= 2
        
        # H_2: u is a valid Laurent polynomial over R
        h2 = False
        if h1:
            try:
                terms = get_laurent_terms(u_expr, x, n)
                h2 = True
            except Exception:
                h2 = False
                
        if not (h1 and h2):
            return [h1, h2, False]
            
        u_is_unit = is_unit_laurent(terms, n)
        u_is_axk = is_form_axk(terms, n)
        
        # The conclusion states: u is a unit iff u = a*x^k for some unit a.
        # The negation of the conclusion is True when the equivalence fails.
        # Since u = a*x^k (with a being a unit) ALWAYS implies u is a unit,
        # the only way the equivalence fails is if u is a unit BUT NOT of the form a*x^k.
        neg_q = u_is_unit and not u_is_axk
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Ring is the ring of Laurent polynomials over R",
    "H_2: u is in the ring",
    "not Q: u is a unit but not of the form a x^k"
]

N_HYP = 2
NEG_Q_INDEX = 2