import sympy

# Top-level setup
# No specific named objects required for this field theory conjecture

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        p, k = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = (int(k) == k) and (k >= 0)
    except Exception:
        h2 = False

    try:
        h3 = True
    except Exception:
        h3 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = int(p**k)
            x = sympy.Symbol('x')
            phi = sympy.cyclotomic_poly(n, x)
            norm = phi.subs(x, 1)
            neg_q = bool(norm != p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: zeta_{p^k} is a primitive p^k-th root of unity",
    "H_3: N denotes the algebraic norm",
    "¬Q: N(1 - zeta_{p^k}) != p"
]

N_HYP = 3
NEG_Q_INDEX = 3