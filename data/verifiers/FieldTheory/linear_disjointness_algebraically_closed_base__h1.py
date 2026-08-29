import sympy
from sympy import minpoly, degree
from sympy.polys.numberfields import primitive_element

# Top-level setup
QQ = sympy.QQ
x = sympy.Symbol('x')

def conditions(witness):
    """
    Verifies that the given witness is a counterexample to the false conjecture.
    The witness should provide generators for the fields E and F over K = Q.
    It can be a tuple (alpha, beta) or a dictionary with keys 'E' and 'F'.
    """
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha', witness.get('E_gen', witness.get('E')))
            beta = witness.get('beta', witness.get('F_gen', witness.get('F')))
        else:
            alpha, beta = witness

        def get_prim(gens):
            if isinstance(gens, (list, tuple)):
                if len(gens) == 0:
                    return sympy.Integer(0)
                elif len(gens) == 1:
                    return sympy.sympify(gens[0])
                else:
                    prim = primitive_element(gens)
                    if isinstance(prim, tuple):
                        return prim[0]
                    return prim
            return sympy.sympify(gens)

        alpha = get_prim(alpha)
        beta = get_prim(beta)
    except Exception:
        return [False, False, False, False]

    # H1: Omega is a field extension of K
    # We use K = Q, E = Q(alpha), F = Q(beta), Omega = Q(alpha, beta).
    # This is valid if alpha and beta are algebraic numbers over Q.
    try:
        poly_alpha = minpoly(alpha)
        poly_beta = minpoly(beta)
        h1 = True
    except Exception:
        h1 = False

    # H2: E and F are subfields of Omega that contain K
    # By our construction, E and F naturally contain Q and are contained in Omega.
    h2 = h1

    # H3: E and F are algebraically disjoint over K
    # Since E and F are algebraic extensions of Q, their transcendence degree over Q is 0.
    # The only algebraically independent subset is the empty set, which is trivially 
    # algebraically independent over F. Thus, they are always algebraically disjoint.
    h3 = h1

    # ¬Q: E and F are NOT linearly disjoint over K
    # For finite extensions, linear disjointness implies dim_K(EF) = dim_K(E) * dim_K(F).
    # If the degree of the compositum is strictly less, they are not linearly disjoint.
    try:
        deg_E = degree(poly_alpha)
        deg_F = degree(poly_beta)
        
        if deg_E == 1 or deg_F == 1:
            neg_q = False
        else:
            prim = primitive_element([alpha, beta])
            if isinstance(prim, tuple):
                prim = prim[0]
            deg_Omega = degree(minpoly(prim))
            neg_q = bool(deg_Omega < deg_E * deg_F)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Omega is a field extension of K",
    "H_2: E and F are subfields of Omega that contain K",
    "H_3: E and F are algebraically disjoint over K",
    "¬Q: E and F are not linearly disjoint over K"
]

N_HYP = 3
NEG_Q_INDEX = 3