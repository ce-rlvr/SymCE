import sympy

# Top-level setup
# No named bindings needed for number theory

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
            q = witness.get('q')
        else:
            p, a, q = witness
    except Exception:
        return [False, False, False, False]

    try:
        if p != int(p):
            h1 = False
        else:
            p_int = int(p)
            h1 = bool(sympy.isprime(p_int) and p_int % 2 != 0)
    except Exception:
        h1 = False

    try:
        if a != int(a) or p != int(p):
            h2 = False
        else:
            a_int = int(a)
            p_int = int(p)
            h2 = bool(a_int % p_int != 0)
    except Exception:
        h2 = False

    try:
        if q != int(q):
            h3 = False
        else:
            q_int = int(q)
            h3 = bool(sympy.isprime(q_int))
    except Exception:
        h3 = False

    try:
        if p != int(p) or q != int(q):
            neg_q = False
        else:
            p_int = int(p)
            q_int = int(q)
            neg_q = bool(p_int % q_int != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is an integer not divisible by p",
    "H_3: q is a prime number",
    "¬Q: p is not congruent to 1 modulo q"
]

N_HYP = 3
NEG_Q_INDEX = 3