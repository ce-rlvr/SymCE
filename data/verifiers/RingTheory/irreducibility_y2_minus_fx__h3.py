import sympy
from sympy import Poly, isprime
from sympy.abc import x, y

# Top-level setup
# (No special groups or matrices needed for this ring theory theorem)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (char, f_expr) where char is the characteristic 
    of the field (0 for QQ, p for GF(p)) and f_expr is a polynomial in x.
    If a single expression is provided, char=0 is assumed.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            char, f_expr = witness
        else:
            char = 0
            f_expr = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field of characteristic not equal to 2
    try:
        if char == 0:
            h1_ok = True
        else:
            h1_ok = bool(isprime(char) and char != 2)
    except Exception:
        h1_ok = False

    # H_2: f(x) is a polynomial over F
    try:
        f_expr_sym = sympy.sympify(f_expr)
        if not f_expr_sym.free_symbols.issubset({x}):
            h2_ok = False
        else:
            if char == 0:
                domain = sympy.QQ
            else:
                domain = sympy.GF(char)
            # This will raise an exception if f_expr_sym cannot be interpreted as a polynomial over the domain
            f_poly = Poly(f_expr_sym, x, domain=domain)
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: y^2 - f(x) is reducible
    try:
        f_expr_sym = sympy.sympify(f_expr)
        if char == 0:
            domain = sympy.QQ
        else:
            domain = sympy.GF(char)
            
        poly_xy = Poly(y**2 - f_expr_sym, x, y, domain=domain)
        factors = poly_xy.factor_list()
        
        # factors[1] is a list of tuples: (factor_poly, multiplicity)
        # The polynomial is reducible if the sum of multiplicities of its non-unit factors is > 1
        num_factors = sum(exp for f, exp in factors[1])
        neg_q_ok = bool(num_factors > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: f(x) is a polynomial over F",
    "¬Q: y^2 - f(x) is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2