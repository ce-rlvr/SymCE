import sympy
from sympy import Poly, GF
from sympy.abc import x
from sympy.ntheory import factorint

x_sym = x

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: m is the minimal polynomial of alpha over F_q",
    "H_3: d is the degree of m",
    "not Q: m does not split completely in F_q_n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get("q")
            m = witness.get("m")
            d = witness.get("d")
            n = witness.get("n")
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            q, m, d, n = witness[:4]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if isinstance(m, str):
            m = sympy.sympify(m)
    except Exception:
        pass

    # H1
    try:
        q_val = int(q)
        if q_val >= 2:
            factors = factorint(q_val)
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2
    try:
        if h1:
            if isinstance(m, sympy.Expr):
                free_syms = list(m.free_symbols)
                gen = free_syms[0] if len(free_syms) == 1 else x
            else:
                gen = x
            p = Poly(m, gen, domain=GF(q_val))
            h2 = bool(p.is_monic and p.is_irreducible)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3
    try:
        d_val = int(d)
        if h2:
            h3 = bool(d_val == p.degree())
        else:
            if isinstance(m, sympy.Expr):
                free_syms = list(m.free_symbols)
                gen = free_syms[0] if len(free_syms) == 1 else x
            else:
                gen = x
            p_any = Poly(m, gen)
            h3 = bool(d_val == p_any.degree())
    except Exception:
        h3 = False

    # neg_Q
    try:
        n_val = int(n)
        if n_val >= 1 and d_val >= 1:
            neg_q = bool(n_val % d_val != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]