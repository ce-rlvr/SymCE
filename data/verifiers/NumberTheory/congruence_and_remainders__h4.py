import sympy

def is_int(x):
    return isinstance(x, (int, sympy.Integer))

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            m = witness['m']
            a = witness['a']
            b = witness['b']
            q1 = witness['q1']
            r1 = witness['r1']
            q2 = witness['q2']
            r2 = witness['r2']
        else:
            m, a, b, q1, r1, q2, r2 = witness
    except Exception:
        return [False] * 5

    try:
        h1 = bool(is_int(m) and m > 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(is_int(a) and is_int(b))
    except Exception:
        h2 = False

    try:
        h3 = bool(is_int(q1) and is_int(r1) and is_int(q2) and is_int(r2) and 
                  a == q1 * m + r1 and b == q2 * m + r2)
    except Exception:
        h3 = False

    try:
        h4 = bool((a - b) % m == 0)
    except Exception:
        h4 = False

    try:
        neg_q = bool(r1 != r2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a and b are integers",
    "H_3: a = q1*m + r1 and b = q2*m + r2 for integers q1, q2, r1, r2",
    "H_4: a == b (mod m)",
    "¬Q: r1 != r2"
]

N_HYP = 4
NEG_Q_INDEX = 4