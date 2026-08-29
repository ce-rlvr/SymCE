import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: The number of distinct Sylow p-subgroups of G is exactly 1",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Parse witness
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, P, p = witness
            p = int(p)
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, P = witness
            order_P = P.order()
            factors = sympy.factorint(order_P)
            if len(factors) == 1:
                p = int(list(factors.keys())[0])
            elif order_P == 1:
                p = 2
                while G.order() % p == 0:
                    p = sympy.nextprime(p)
            else:
                p = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if p is None or p <= 1:
            h2 = False
        elif not isinstance(P, PermutationGroup):
            h2 = False
        elif not all(g in G for g in P.generators):
            h2 = False
        else:
            k = 0
            while G.order() % (p**(k+1)) == 0:
                k += 1
            h2 = (P.order() == p**k)
    except Exception:
        h2 = False

    # H_3: The number of distinct Sylow p-subgroups of G is exactly 1
    try:
        if p is None or p <= 1:
            h3 = False
        elif sympy.isprime(p):
            if G.order() % p != 0:
                h3 = True
            else:
                S = G.sylow_subgroup(p)
                h3 = S.is_normal(G)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: P is not a normal subgroup of G
    try:
        q = P.is_normal(G)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]