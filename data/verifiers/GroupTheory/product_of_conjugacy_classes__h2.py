import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if len(witness) == 3:
            G, K, L = witness
            KL_given = None
        elif len(witness) == 4:
            G, K, L, KL_given = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            for k in K:
                if k not in G:
                    h1 = False
            for l in L:
                if l not in G:
                    h1 = False
    except Exception:
        h1 = False

    # H_2: L is a conjugacy class of G
    try:
        if not L:
            h2 = False
        else:
            rep = list(L)[0]
            conj_class = set(g * rep * ~g for g in G.generate())
            h2 = (set(L) == conj_class)
    except Exception:
        h2 = False

    # H_3: KL = {kl | k in K, l in L}
    try:
        KL = set(k * l for k in K for l in L)
        if KL_given is not None:
            h3 = (set(KL_given) == KL)
        else:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: KL is not a union of conjugacy classes of G
    try:
        neg_q = False
        for x in KL:
            for g in G.generate():
                if g * x * ~g not in KL:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: L is a conjugacy class of G",
    "H_3: KL = {kl | k in K, l in L}",
    "¬Q: KL is not a union of conjugacy classes of G"
]

N_HYP = 3
NEG_Q_INDEX = 3