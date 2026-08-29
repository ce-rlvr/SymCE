import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def highest_power(n, p):
    if p <= 1:
        return 0
    k = 0
    while n % (p**(k+1)) == 0:
        k += 1
    return k

def is_sylow_p_subgroup(P, G, p):
    if not isinstance(P, PermutationGroup):
        return False
    if not P.is_subgroup(G):
        return False
    k = highest_power(G.order(), p)
    return P.order() == p**k

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            P = witness.get('P')
            Q = witness.get('Q')
            p = witness.get('p')
        else:
            G, H, P, Q, p = witness
    except Exception:
        return [False, False, False, False]

    try:
        p = int(p)
        if p <= 1:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are finite groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = is_sylow_p_subgroup(P, G, p)
    except Exception:
        h2 = False

    # H_3: Q is a Sylow p-subgroup of H
    try:
        h3 = is_sylow_p_subgroup(Q, H, p)
    except Exception:
        h3 = False

    # ¬Q: P x Q is not a Sylow p-subgroup of G x H
    try:
        if not (isinstance(P, PermutationGroup) and isinstance(Q, PermutationGroup)):
            neg_q = False
        else:
            k_GH = highest_power(G.order() * H.order(), p)
            neg_q = (P.order() * Q.order()) != (p ** k_GH)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Q is a Sylow p-subgroup of H",
    "¬Q: P x Q is not a Sylow p-subgroup of G x H"
]

N_HYP = 3
NEG_Q_INDEX = 3