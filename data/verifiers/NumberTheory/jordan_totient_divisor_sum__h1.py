import sympy

def J(k, d):
    d = int(d)
    if d == 1:
        return 1
    factors = sympy.factorint(d)
    res = d**k
    for p in factors:
        res = res * (p**k - 1) // (p**k)
    return res

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            k = witness['k']
        else:
            n, k = witness
    except Exception:
        return [False, False]

    # H_1: k is a positive integer
    try:
        h1 = bool((isinstance(k, int) or isinstance(k, sympy.Integer)) and k > 0)
    except Exception:
        h1 = False

    # ¬Q: \sum_{d|n} J_k(d) != n^k
    try:
        if n == 0:
            # 0 has infinitely many divisors, so the sum is undefined/divergent
            neg_q = True
        else:
            divs = sympy.divisors(n)
            lhs = sum(J(k, d) for d in divs)
            rhs = n**k
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: sum_{d|n} J_k(d) != n^k"
]

N_HYP = 1
NEG_Q_INDEX = 1