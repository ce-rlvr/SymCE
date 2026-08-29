import sympy
from sympy import symbols, Poly, groebner, ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: F is a free R-module of finite rank n",
    "H_2: M is a submodule of F",
    "¬Q: M is not a free R-module of rank k <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    witness is expected to be a tuple: (vars, domain, n, M_gens)
    where:
      - vars is a tuple of sympy symbols, e.g., (x,)
      - domain is a sympy domain or string, e.g., 'ZZ'
      - n is the rank of the free module F (must be 1 for our freeness check)
      - M_gens is a list of tuples of length n, representing generators of M
    Example: ((x,), 'ZZ', 1, [(2,), (x,)])
    """
    try:
        vars, domain, n, M_gens = witness
    except Exception:
        return [False, False, False]
        
    # H1: F is a free R-module of finite rank n
    try:
        if not isinstance(vars, tuple) or len(vars) == 0:
            h1 = False
        elif not isinstance(n, int) or n < 1:
            h1 = False
        else:
            # Check if domain is valid by creating a zero polynomial
            Poly(0, *vars, domain=domain)
            h1 = True
    except Exception:
        h1 = False

    # H2: M is a submodule of F
    try:
        if not isinstance(M_gens, list) or len(M_gens) == 0:
            h2 = False
        else:
            h2 = True
            for vec in M_gens:
                if not isinstance(vec, (list, tuple)) or len(vec) != n:
                    h2 = False
                    break
                for g in vec:
                    # Check if g is a valid element in the polynomial ring
                    Poly(g, *vars, domain=domain)
    except Exception:
        h2 = False

    # neg_Q: M is NOT a free R-module of rank k <= n
    try:
        if h1 and h2:
            if n == 1:
                # For n=1, M is an ideal in the polynomial ring.
                # Since the ring is a domain, M is free iff it is principal.
                # M is principal iff its reduced Groebner basis has length <= 1.
                gens = [vec[0] for vec in M_gens]
                G = groebner(gens, *vars, domain=domain)
                neg_q = len(G) > 1
            else:
                # For n > 1, we don't have a simple freeness check implemented.
                # A valid counterexample can just use n=1.
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]