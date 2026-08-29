import sympy
from sympy.ntheory import isprime

# Top-level setup
# Witnesses are expected to be tuples (n, m, p) representing:
# R = Z/nZ
# m_ideal = mZ/nZ (a maximal ideal, so m is a prime dividing n)
# M = Z/pZ (a simple R-module, so p is a prime dividing n)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = int(witness['n'])
            m = int(witness['m'])
            p = int(witness['p'])
        else:
            n, m, p = witness
            n = int(n)
            m = int(m)
            p = int(p)
    except Exception:
        return [False, False]

    try:
        # M is a simple R-module (and R, m are valid)
        # n > 1 ensures Z/nZ is a valid ring
        # isprime(m) and n % m == 0 ensures mZ/nZ is a maximal ideal of Z/nZ
        # isprime(p) and n % p == 0 ensures Z/pZ is a simple Z/nZ-module
        h1 = (n > 1) and isprime(m) and (n % m == 0) and isprime(p) and (n % p == 0)
    except Exception:
        h1 = False

    try:
        # M is isomorphic to R/m iff p == m
        neg_q = (p != m)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a simple R-module (and R, m are valid)",
    "¬Q: M is not isomorphic to R/m as an R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1