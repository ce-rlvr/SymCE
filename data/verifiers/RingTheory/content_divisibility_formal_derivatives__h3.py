import sympy
from sympy import Poly, Symbol, Rational, Integer
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, Poly):
            f = witness
        elif hasattr(witness, "free_symbols"):
            free = witness.free_symbols
            if not free:
                gen = Symbol("x")
            elif len(free) == 1:
                gen = list(free)[0]
            else:
                if Symbol("x") in free:
                    gen = Symbol("x")
                else:
                    gen = list(free)[0]
            f = Poly(witness, gen)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        domain = f.domain
        if getattr(domain, "is_UFD", False):
            h1 = True
        elif domain.is_IntegerRing or domain.is_RationalField:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: f in R[x] is a non-constant polynomial
    try:
        if f.degree() > 0:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The content c(f) does not divide the content c(f') in R
    try:
        c_f = f.content()
        df = f.diff()
        c_df = df.content()
        
        if c_f == 0:
            divides = (c_df == 0)
        else:
            try:
                # Check exact divisibility in the domain R
                q = f.domain.exquo(c_df, c_f)
                divides = True
            except Exception:
                divides = False
                
        neg_q = not divides
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-constant polynomial over R",
    "¬Q: The content c(f) does not divide the content c(df) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2