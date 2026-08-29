import sympy
from sympy import Poly, Symbol, symbols, diff
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t, alpha = symbols('x y z t alpha')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture:
    "Over any field F, if alpha is algebraic over F with minimal polynomial m(x), 
    then all roots of m(x) in its splitting field have multiplicity 1."
    (The dropped hypothesis is that F is a perfect field).
    
    The witness should be a dictionary or tuple specifying:
      - poly: the minimal polynomial m(x) (e.g., x**2 - t)
      - var: the main variable (e.g., x)
      - p: the characteristic of the field (a prime number, e.g., 2)
    """
    try:
        if isinstance(witness, dict):
            poly_expr = witness['poly']
            var = witness['var']
            p = witness['p']
        else:
            poly_expr, var, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: p is prime (so F is a valid field of characteristic p)
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # Determine the variables involved to construct the polynomial ring
    try:
        syms = list(poly_expr.free_symbols)
        if var not in syms:
            syms.append(var)
    except Exception:
        syms = [var]

    poly_obj = None
    
    # H2: poly has degree >= 1 in var (alpha is algebraic)
    try:
        poly_obj = Poly(poly_expr, *syms, domain=sympy.GF(p))
        h2 = bool(poly_obj.degree(var) >= 1)
    except Exception:
        h2 = False
        
    # H3: poly is irreducible over GF(p) in all its variables
    # By Gauss's Lemma, this implies it is irreducible over the fraction field of the other variables,
    # making it the minimal polynomial of its root.
    try:
        if poly_obj is not None:
            h3 = bool(poly_obj.is_irreducible)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: The formal derivative of poly with respect to var is 0 mod p.
    # For an irreducible polynomial, this is equivalent to having roots of multiplicity > 1 in its splitting field.
    try:
        deriv = diff(poly_expr, var)
        deriv_obj = Poly(deriv, *syms, domain=sympy.GF(p))
        neg_q = bool(deriv_obj.is_zero)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field (characteristic p is prime)",
    "H_2: alpha is algebraic over F (m(x) is non-constant)",
    "H_3: m(x) is the minimal polynomial of alpha over F (irreducible)",
    "¬Q: m(x) has roots of multiplicity > 1 in its splitting field"
]

N_HYP = 3
NEG_Q_INDEX = 3