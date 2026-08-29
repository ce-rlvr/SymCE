import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            N = witness.get('N')
        else:
            G, p, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number dividing the order of G
    try:
        h2 = bool(isprime(p) and (G.order() % p == 0))
    except Exception:
        h2 = False

    # ¬Q: N is not a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup):
            neg_q = False
        else:
            try:
                is_sub = N.is_subgroup(G)
            except Exception:
                is_sub = False
            
            if not is_sub:
                neg_q = True
            else:
                neg_q = not G.is_normal(N)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "¬Q: N is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2