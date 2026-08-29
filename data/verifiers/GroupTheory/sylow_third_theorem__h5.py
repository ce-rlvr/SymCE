import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            p = witness['p']
            n = witness['n']
            m = witness['m']
            n_p = witness['n_p']
        else:
            G, p, n, m, n_p = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = bool(isinstance(G, PermutationGroup))
    except Exception:
        h1 = False

    # H2: The order of G is p^n * m
    try:
        h2 = bool(G.order() == (p**n) * m)
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = bool(sympy.isprime(p))
    except Exception:
        h3 = False

    # H4: p does not divide m
    try:
        h4 = bool(m % p != 0)
    except Exception:
        h4 = False

    # neg_Q: not (n_p divides m and n_p is congruent to 1 modulo p)
    try:
        if n_p == 0:
            divides = False
        else:
            divides = bool(m % n_p == 0)
        congruent = bool(n_p % p == 1)
        neg_q = not (divides and congruent)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p^n * m",
    "H_3: p is a prime number",
    "H_4: p does not divide m",
    "¬Q: n_p does not divide m or n_p is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4