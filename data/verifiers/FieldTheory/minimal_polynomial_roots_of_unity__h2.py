import sympy
from sympy import Symbol, cyclotomic_poly, minpoly, sympify
from sympy.abc import x

# Top-level setup for witness expressions
I = sympy.I
pi = sympy.pi
exp = sympy.exp
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    
    The witness is expected to provide `n` and `zeta` (and optionally `Phi`).
    It can be a tuple (n, zeta) or (n, Phi, zeta), a dict, or an object.
    """
    n = None
    Phi = None
    zeta = None
    
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            zeta = witness.get('zeta')
            Phi = witness.get('Phi')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                n, zeta = witness
            elif len(witness) == 3:
                n, Phi, zeta = witness
        else:
            n = getattr(witness, 'n', None)
            zeta = getattr(witness, 'zeta', None)
            Phi = getattr(witness, 'Phi', None)
    except Exception:
        pass

    if n is None or zeta is None:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        if int(n) == n and n > 0:
            n = int(n)
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False]

    # Safely resolve Phi if not explicitly provided
    try:
        if Phi is None:
            Phi = cyclotomic_poly(n, x)
    except Exception:
        pass

    if Phi is None:
        return [False, False, False]

    # H_2: Phi_n(x) is the n-th cyclotomic polynomial over Z
    try:
        expected_Phi = cyclotomic_poly(n, x)
        phi_expr = sympify(Phi)
        if hasattr(phi_expr, 'as_expr'):
            phi_expr = phi_expr.as_expr()
            
        free_syms = phi_expr.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
            phi_expr = phi_expr.subs(sym, x)
            
        h2 = sympy.expand(phi_expr - expected_Phi) == 0
    except Exception:
        h2 = False

    # not Q: Phi_n(x) is NOT the minimal polynomial of zeta_n over Q
    try:
        min_p = minpoly(zeta, x)
        neg_q = sympy.expand(phi_expr - min_p) != 0
    except Exception:
        # If minpoly fails, zeta is not algebraic over Q, so Phi cannot be its minimal polynomial
        try:
            neg_q = sympy.expand(phi_expr) != 0
        except Exception:
            neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial over Z",
    "not Q: Phi_n(x) is not the minimal polynomial of zeta_n over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2