import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

# Top-level setup: named object bindings
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
    if isinstance(witness, dict):
        G = witness.get('G')
        p = witness.get('p')
        N = witness.get('N')
        P = witness.get('P')
    elif isinstance(witness, (tuple, list)) and len(witness) == 4:
        G, p, N, P = witness
    else:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and N.is_subgroup(G):
            h3 = True
            for g in G.generators:
                g_inv = ~g
                for n in N.generators:
                    if (g * n * g_inv) not in N:
                        h3 = False
                        break
                if not h3:
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: The index of N in G is a power of p
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(p, (int, sympy.Integer)) and p > 1:
            if G.order() % N.order() != 0:
                h4 = False
            else:
                idx = G.order() // N.order()
                temp = idx
                while temp % p == 0:
                    temp //= p
                h4 = (temp == 1)
        else:
            h4 = False
    except Exception:
        h4 = False

    # ¬Q: G != PN
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(P, PermutationGroup):
            if P.is_subgroup(G) and N.is_subgroup(G):
                gens = list(P.generators) + list(N.generators)
                PN = PermutationGroup(gens)
                neg_q = (PN.order() != G.order())
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N is a normal subgroup of G",
    "H_4: The index of N in G is a power of p",
    "¬Q: G != PN"
]

N_HYP = 4
NEG_Q_INDEX = 4