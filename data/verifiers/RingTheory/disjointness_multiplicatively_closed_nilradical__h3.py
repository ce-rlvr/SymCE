import sympy
from sympy.ntheory import factorint
from sympy import Rational

# Top-level setup for witness expressions
QQ = sympy.QQ
ZZ = sympy.ZZ
Q = sympy.QQ
Z = sympy.ZZ

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def _parse_witness(witness):
    n, S = witness
    if isinstance(n, str) and n.upper().startswith("Z"):
        n = int(n[1:])
    return n, S

def conditions(witness) -> list[bool]:
    # H1: R is a commutative ring, S is a subset
    try:
        n, S = _parse_witness(witness)
        if n == sympy.ZZ:
            h1 = isinstance(S, (list, set, tuple)) and all(isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer) for x in S)
        elif n == sympy.QQ:
            h1 = isinstance(S, (list, set, tuple))
        else:
            h1 = isinstance(n, int) and n >= 2 and isinstance(S, (list, set, tuple)) and all(isinstance(x, int) and 0 <= x < n for x in S)
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        n, S = _parse_witness(witness)
        S_set = set(S)
        if n in (sympy.QQ, sympy.ZZ):
            h2 = all((a * b) in S_set for a in S_set for b in S_set)
        else:
            h2 = all((a * b) % n in S_set for a in S_set for b in S_set)
    except Exception:
        h2 = False

    # neg_Q: The intersection of S and the nilradical of R is NOT empty
    try:
        n, S = _parse_witness(witness)
        S_set = set(S)
        if n in (sympy.QQ, sympy.ZZ):
            # In ZZ and QQ, the only nilpotent element is 0
            neg_q = 0 in S_set
        else:
            # In Z/nZ, an element is nilpotent iff it is divisible by all prime factors of n
            primes = factorint(n).keys()
            neg_q = any(all(x % p == 0 for p in primes) for x in S_set)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring and S is a subset of R",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The intersection of S and the nilradical of R is not empty"
]

N_HYP = 2
NEG_Q_INDEX = 2