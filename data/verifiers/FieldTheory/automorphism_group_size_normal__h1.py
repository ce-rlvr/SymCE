import sympy
from sympy import Symbol, Poly, factor_list, RootOf, degree

x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be an irreducible polynomial in x over Q,
    representing the finite separable field extension K = Q(alpha) / Q,
    where alpha is a root of the polynomial.
    """
    try:
        if hasattr(witness, 'as_expr'):
            expr = witness.as_expr()
        else:
            expr = witness
            
        p = Poly(expr, x, domain='QQ')
        h1 = p.is_irreducible and p.degree() >= 1
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            deg = p.degree()
            separable_degree = deg
            
            alpha = RootOf(expr, x, 0)
            facs = factor_list(expr, x, extension=alpha)[1]
            
            aut_group_size = 0
            for base, exp in facs:
                if degree(base, x) == 1:
                    aut_group_size += 1
            
            neg_q = (aut_group_size != separable_degree)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (K:F)_s denotes the separable degree of K over F",
    "¬Q: The order of the automorphism group Aut(K/F) is not exactly equal to (K:F)_s"
]

N_HYP = 1
NEG_Q_INDEX = 1