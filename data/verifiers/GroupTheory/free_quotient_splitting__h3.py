import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    G_elements = set()
    N_elements = set()
    identity = None
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and h1:
            G_elements = set(G.elements)
            N_elements = set(N.elements)
            if N_elements.issubset(G_elements):
                # Find identity
                for g in G_elements:
                    if g * g == g:
                        identity = g
                        break
                
                if identity is not None and identity in N_elements:
                    is_normal = True
                    for g in G_elements:
                        g_inv = ~g
                        for n in N_elements:
                            if g * n * g_inv not in N_elements:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                    h2 = is_normal
    except Exception:
        h2 = False
        
    # neg_Q: The sequence does not split
    # i.e., there is NO subgroup H of G such that |H| = |G|/|N| and H \cap N = {1}.
    try:
        neg_q = False
        if h1 and h2:
            target_order = len(G_elements) // len(N_elements)
            if target_order == 1:
                neg_q = False
            else:
                allowed = [g for g in G_elements if g not in N_elements or g == identity]
                allowed_set = set(allowed)
                
                def get_subgroup(gens):
                    S = set(gens)
                    S.add(identity)
                    added = True
                    while added:
                        added = False
                        new_elements = set()
                        for x in S:
                            for y in S:
                                xy = x * y
                                if xy not in S and xy not in new_elements:
                                    if xy not in allowed_set:
                                        return None
                                    new_elements.add(xy)
                                    if len(S) + len(new_elements) > target_order:
                                        return None
                        if new_elements:
                            S.update(new_elements)
                            added = True
                    return S
                
                cyclic_subgroups = []
                found_complement = False
                for g in allowed:
                    if g == identity: 
                        continue
                    H = get_subgroup([g])
                    if H is not None:
                        if len(H) == target_order:
                            found_complement = True
                            break
                        cyclic_subgroups.append(H)
                
                if not found_complement:
                    known_subgroups = set()
                    known_subgroups.add(frozenset([identity]))
                    for H1 in cyclic_subgroups:
                        known_subgroups.add(frozenset(H1))
                        
                    new_subgroups = list(known_subgroups)
                    while new_subgroups and not found_complement:
                        if len(known_subgroups) > 2000:
                            break
                        next_new = []
                        for H in new_subgroups:
                            for C in cyclic_subgroups:
                                if not C.issubset(H):
                                    gens = list(H | C)
                                    H_new = get_subgroup(gens)
                                    if H_new is not None:
                                        fs = frozenset(H_new)
                                        if fs not in known_subgroups:
                                            if len(fs) == target_order:
                                                found_complement = True
                                                break
                                            known_subgroups.add(fs)
                                            next_new.append(fs)
                            if found_complement:
                                break
                        new_subgroups = next_new
                
                neg_q = not found_complement
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: G is not isomorphic to N \\rtimes (G/N) (the short exact sequence does not split)"
]

N_HYP = 2
NEG_Q_INDEX = 2