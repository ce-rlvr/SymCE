import sympy

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness['n']
            p = witness['p']
        else:
            n, p = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 0
    except Exception:
        h1 = False

    try:
        if not isinstance(p, (int, sympy.Integer)) or p <= 0:
            neg_q = False
        else:
            n_int = int(n)
            p_int = int(p)
            b_np = sympy.bell(n_int + p_int)
            b_n = sympy.bell(n_int)
            b_np1 = sympy.bell(n_int + 1)
            neg_q = (b_np % p_int) != ((b_n + b_np1) % p_int)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a non-negative integer",
    "¬Q: B_{n+p} is not congruent to B_n + B_{n+1} mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1