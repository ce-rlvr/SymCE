import sympy as sp
from sympy import Poly
from sympy.abc import x

# Top-level setup for potential witness expressions
QQ = sp.QQ
ZZ = sp.ZZ
GF = sp.GF

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either:
      - A tuple (f, n) where f is a sympy Poly (domain inferred) and n is an integer.
      - A tuple (F, f, n) where F is a sympy Domain, f is a polynomial/expression, and n is an integer.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f_in, n = witness
                if isinstance(f_in, sp.Poly):
                    f = f_in
                    F = f.domain
                else:
                    free = getattr(f_in, "free_symbols", set())
                    gen = list(free)[0] if free else x
                    f = sp.Poly(f_in, gen)
                    F = f.domain
            elif len(witness) == 3:
                F, f_expr, n = witness
                if isinstance(f_expr, sp.Poly):
                    f = f_expr
                else:
                    free = getattr(f_expr, "free_symbols", set())
                    gen = list(free)[0] if free else x
                    f = sp.Poly(f_expr, gen, domain=F)
            else:
                return [False, False]
        else:
            return [False, False]
            
        n = int(n)
    except Exception:
        return [False, False]

    # H_1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails at the witness
    # The conclusion states that every equivalence class in F[x]/<f(x)> contains exactly one 
    # polynomial r(x) such that r(x) = 0 or deg(r(x)) < n.
    # This holds if and only if f(x) != 0 and (deg(f) == n or (deg(f) == 0 and n <= 0)).
    try:
        if f.is_zero:
            neg_q = True
        else:
            m = f.degree()
            conclusion_holds = (m == n) or (m == 0 and n <= 0)
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The equivalence classes do not all contain exactly one representative of degree < n (or 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1