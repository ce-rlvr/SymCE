import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        G, p = witness
    except Exception:
        return [False, False]

    try:
        order = G.order() if callable(G.order) else G.order
        h1 = isprime(p) and (order % p == 0)
    except Exception:
        h1 = False

    try:
        # The number of Sylow p-subgroups is exactly 1 if and only if 
        # the Sylow p-subgroup is a normal subgroup of G.
        P = G.sylow_subgroup(p)
        is_normal = True
        for g in G.generators:
            for h in P.generators:
                conj = g * h * (~g)
                if conj not in P:
                    is_normal = False
                    break
            if not is_normal:
                break
        neg_q = is_normal
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "¬Q: The number of Sylow p-subgroups of G is exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
