import sympy

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            p = witness['p']
        elif hasattr(witness, 'a') and hasattr(witness, 'p'):
            a = witness.a
            p = witness.p
        else:
            a, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(sympy.n_order(a, p) == 4)
    except Exception:
        h2 = False

    try:
        neg_q = bool((a**2) % p != (-1) % p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: The order of a modulo p is exactly 4",
    "¬Q: a^2 is not congruent to -1 modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2