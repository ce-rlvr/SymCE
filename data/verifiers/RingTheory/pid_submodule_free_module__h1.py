import sympy
from sympy import symbols

# Top-level setup: named object bindings that the witness expression may reference.
# We define some common variables for polynomial rings.
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The expected witness format is a tuple: (n, vars, M_gens)
    where:
      - n is the rank of the free module F (we only support checking freeness for n=1).
      - vars is a tuple of SymPy symbols representing the polynomial ring R = QQ[vars].
      - M_gens is a list of n-tuples of polynomials in R, generating the submodule M.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        n, vars, M_gens = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a free R-module of finite rank n
    # We interpret R as the polynomial ring QQ[vars]. F = R^n is free of rank n.
    try:
        h1 = (isinstance(n, int) and n >= 1 and 
              isinstance(vars, (list, tuple)) and 
              all(isinstance(v, sympy.Symbol) for v in vars))
    except Exception:
        h1 = False
        
    # H_2: M is a submodule of F
    # M_gens must be a list of n-tuples of valid polynomials in vars.
    try:
        h2 = True
        if not isinstance(M_gens, (list, tuple)):
            h2 = False
        else:
            for gen in M_gens:
                if not isinstance(gen, (list, tuple)) or len(gen) != n:
                    h2 = False
                    break
                for poly in gen:
                    p = sympy.sympify(poly)
                    if not isinstance(p, sympy.Expr):
                        h2 = False
                        break
                    if not p.free_symbols.issubset(set(vars)):
                        h2 = False
                        break
                    if vars:
                        if not p.is_polynomial(*vars):
                            h2 = False
                            break
                    else:
                        if not p.is_number:
                            h2 = False
                            break
    except Exception:
        h2 = False
        
    # ¬Q: M is NOT a free R-module of rank <= n
    # For n=1, M is an ideal in the integral domain QQ[vars].
    # An ideal in an integral domain is a free module iff it is principal.
    # It is principal iff its reduced Groebner basis has length 1 (or 0 if the zero ideal).
    try:
        neg_q = False
        if h1 and h2 and n == 1:
            gens = [sympy.sympify(g[0]) for g in M_gens]
            # Remove zero generators
            gens = [g for g in gens if g != 0]
            if not gens:
                # The zero ideal is free of rank 0 <= 1
                neg_q = False
            else:
                # Compute the reduced Groebner basis over QQ
                gb = sympy.groebner(gens, *vars, domain='QQ')
                if len(gb) > 1:
                    # Not principal, hence not free
                    neg_q = True
                else:
                    # Principal, hence free of rank 1 <= n
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free R-module of finite rank n",
    "H_2: M is a submodule of F",
    "¬Q: M is not a free R-module of rank <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2