import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_normal(H, G):
    try:
        if hasattr(H, 'is_normal'):
            res = H.is_normal(G)
            if isinstance(res, bool):
                return res
    except Exception:
        pass
    try:
        if not H.is_subgroup(G):
            return False
        H_elems = set(H.elements)
        for g in G.generators:
            try:
                g_inv = ~g
            except Exception:
                g_inv = g**-1
            for h in H.generators:
                if g * h * g_inv not in H_elems:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, N, M = witness
            elif len(witness) == 2:
                N, M = witness
                G = PermutationGroup(list(N.generators) + list(M.generators))
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = check_normal(N, G)
    except Exception:
        h1 = False

    # H_2: M is a normal subgroup of G
    try:
        h2 = check_normal(M, G)
    except Exception:
        h2 = False

    # H_3: The intersection of N and M contains only the identity element
    try:
        intersection = set(N.elements).intersection(set(M.elements))
        if len(intersection) != 1:
            h3 = False
        else:
            e = list(intersection)[0]
            if hasattr(G, 'identity') and e == G.identity:
                h3 = True
            elif e * e == e:
                h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False

    # ¬Q: There exist n in N and m in M such that nm != mn
    try:
        neg_q = False
        for n in N.elements:
            for m in M.elements:
                if n * m != m * n:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: M is a normal subgroup of G",
    "H_3: The intersection of N and M contains only the identity element",
    "¬Q: There exist n in N and m in M such that nm != mn"
]

N_HYP = 3
NEG_Q_INDEX = 3