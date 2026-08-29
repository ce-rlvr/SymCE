import sympy
from sympy import symbols, Poly, Integer, ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# (No specific groups needed for this ring theory theorem, but we provide standard symbols)

def conditions(witness) -> list[bool]:
    w = witness
    
    # Extract element if witness is a tuple like (R, p)
    if isinstance(w, (tuple, list)) and len(w) == 2:
        w = w[1]
        
    # Try to parse witness into a standard form (int or Poly)
    if isinstance(w, sympy.Expr) and not isinstance(w, sympy.Poly):
        free = w.free_symbols
        if len(free) == 1:
            try:
                w = sympy.Poly(w, domain='QQ')
            except Exception:
                pass
        elif len(free) == 0:
            try:
                if w.is_integer:
                    w = int(w)
            except Exception:
                pass

    # H1: R is a Principal Ideal Domain (PID)
    h1_ok = False
    try:
        if isinstance(w, (int, sympy.Integer)):
            h1_ok = True
        elif isinstance(w, sympy.Poly):
            # F[x] is a PID if F is a field and there is exactly 1 generator
            if len(w.gens) == 1 and w.domain.is_Field:
                h1_ok = True
    except Exception:
        pass

    # H2: p is a non-zero element of R
    h2_ok = False
    try:
        if isinstance(w, (int, sympy.Integer)):
            h2_ok = (int(w) != 0)
        elif isinstance(w, sympy.Poly):
            h2_ok = not w.is_zero
    except Exception:
        pass

    # neg_Q: p is NOT an irreducible element of R
    neg_q_ok = False
    try:
        if isinstance(w, (int, sympy.Integer)):
            # In ZZ, irreducible elements are primes (or their negatives)
            is_irred = sympy.isprime(abs(int(w)))
            neg_q_ok = not is_irred
        elif isinstance(w, sympy.Poly):
            is_irred = w.is_irreducible
            neg_q_ok = not is_irred
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Principal Ideal Domain (PID)",
    "H_2: p is a non-zero element of R",
    "¬Q: p is not an irreducible element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2