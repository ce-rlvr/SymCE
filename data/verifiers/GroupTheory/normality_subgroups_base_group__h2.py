import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(H, G):
    try:
        return all(G.contains(g) for g in H.generators)
    except Exception:
        return False

def is_normal(H, G):
    if not is_subgroup(H, G):
        return False
    try:
        for g in G.generators:
            for h in H.generators:
                if not H.contains(g * h * ~g):
                    return False
                if not H.contains(~g * h * g):
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N, H, M = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a group that is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        h1_ok = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            if is_subgroup(N, G) and is_normal(N, G) and is_subgroup(H, G):
                # For finite groups, N normal, H subgroup, and |N|*|H| == |G| implies N \cap H = {1} and NH = G
                if N.order() * H.order() == G.order():
                    h1_ok = True
    except Exception:
        h1_ok = False

    # Conclusion: M is a normal subgroup of G if and only if M is a normal subgroup of N and hMh^{-1} = M for all h \in H
    try:
        neg_q_ok = False
        if isinstance(M, PermutationGroup):
            P = is_normal(M, G)
            
            Q = False
            if is_normal(M, N):
                Q = True
                for h in H.generators:
                    for m in M.generators:
                        if not M.contains(h * m * ~h):
                            Q = False
                            break
                        if not M.contains(~h * m * h):
                            Q = False
                            break
                    if not Q:
                        break
            
            # The conclusion is P <-> Q. It fails if P != Q.
            neg_q_ok = (P != Q)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "¬Q: It is not the case that (M is normal in G iff M is normal in N and normalized by H)"
]

N_HYP = 1
NEG_Q_INDEX = 1