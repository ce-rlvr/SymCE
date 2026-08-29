import sympy
from sympy import cos, pi, minpoly, totient, cyclotomic_poly, degree, expand

# Top-level setup for named object bindings
# (No specific group or matrix bindings are required for this field theory conjecture)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the conjecture.
    The witness should be a tuple: (n, Psi)
    where n is an integer and Psi is a SymPy expression representing the polynomial.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        n, Psi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is an integer strictly greater than 2
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 2
    except Exception:
        h1 = False
        
    # H_2: Psi_n(x) is the minimal polynomial of 2 cos(2pi/n) over Q
    try:
        # Convert Psi to a standard expression in variable 'x'
        Psi_expr = Psi.as_expr() if hasattr(Psi, 'as_expr') else Psi
        psi_syms = list(Psi_expr.free_symbols)
        x = sympy.Symbol('x')
        psi_sym = psi_syms[0] if psi_syms else x
        Psi_x = Psi_expr.subs(psi_sym, x)
        
        # Compute the true minimal polynomial over Q
        true_minpoly = minpoly(2 * cos(2 * pi / n), x)
        
        # Check if the provided Psi matches the true minimal polynomial
        h2 = expand(true_minpoly - Psi_x) == 0
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion FAILS at the witness.
    # Conclusion: The degree of Psi_n(x) is phi(n)/2, and it satisfies Phi_n(x) = x^(phi(n)/2) Psi_n(x + x^-1)
    try:
        phi_n = totient(n)
        deg_expected = phi_n // 2
        
        # Check if the degree is exactly phi(n)/2
        deg_Psi = degree(Psi_x, x)
        deg_ok = (deg_Psi == deg_expected)
        
        # Check the relation Phi_n(x) = x^(phi(n)/2) Psi_n(x + x^-1)
        Phi_n = cyclotomic_poly(n, x)
        rel_expr = (x**deg_expected) * Psi_x.subs(x, x + 1/x)
        
        diff = expand(Phi_n - rel_expr)
        rel_ok = (diff == 0)
        
        # neg_Q is True if the conclusion fails (i.e., either condition is not met)
        neg_Q = not (deg_ok and rel_ok)
    except Exception:
        neg_Q = False
        
    return [bool(h1), bool(h2), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "H_2: Psi_n(x) is the minimal polynomial of 2 cos(2pi/n) over Q",
    "¬Q: The degree of Psi_n(x) is not phi(n)/2, or it does not satisfy Phi_n(x) = x^(phi(n)/2) Psi_n(x + x^-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2