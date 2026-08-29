import sympy
from sympy import Poly
from sympy.abc import x, y, z

# Top-level setup
# Standard symbols are provided for convenience.
# The witness is expected to be a tuple of two polynomial expressions (f, g)
# representing the minimal polynomials of α and β over F.

CONDITION_LABELS = [
    "H_1: α and β are algebraic over F (minimal polynomials are irreducible)",
    "H_2: The minimal polynomial of α over F is distinct from the minimal polynomial of β over F",
    "¬Q: The minimal polynomials have a common root in some extension field"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        f_expr, g_expr = witness
        
        # Extract variables to ensure both polynomials use the same generator
        expr_f = sympy.sympify(f_expr)
        expr_g = sympy.sympify(g_expr)
        free_symbols = expr_f.free_symbols.union(expr_g.free_symbols)
        
        if not free_symbols:
            # If there are no variables, they are constants, so not valid minimal polynomials
            return [False, False, False]
            
        gen = list(free_symbols)[0]
        
        f = Poly(expr_f, gen)
        g = Poly(expr_g, gen)
        
        # Ensure we are working over a field so that scalar multiples don't affect irreducibility
        if f.domain.is_Ring and not f.domain.is_Field:
            f = f.set_domain(f.domain.get_field())
        if g.domain.is_Ring and not g.domain.is_Field:
            g = g.set_domain(g.domain.get_field())
            
        # H_1: α and β are algebraic over F
        # This implies their minimal polynomials exist, are non-constant, and are irreducible over F.
        h1 = f.degree() >= 1 and g.degree() >= 1 and f.is_irreducible and g.is_irreducible
        
        # H_2: The minimal polynomial of α over F is distinct from the minimal polynomial of β over F
        h2 = f != g
        
        # ¬Q: The minimal polynomials have a common root in some extension field
        # This is equivalent to them having a non-constant GCD over F.
        neg_q = f.gcd(g).degree() >= 1
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]