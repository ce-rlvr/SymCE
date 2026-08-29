import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A3 = AlternatingGroup(3)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False] * 5

    def is_subgroup(sub, grp):
        for g in sub.generators:
            if not grp.contains(g):
                return False
        return True

    def is_normal(sub, grp):
        if not is_subgroup(sub, grp): 
            return False
        for n in sub.generators:
            for g in grp.generators:
                if not sub.contains(g * n * (~g)):
                    return False
                if not sub.contains((~g) * n * g):
                    return False
        return True

    # H_1: G, N, and H are permutation groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = h1 and is_normal(N, G)
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = h1 and is_subgroup(H, G)
    except Exception:
        h3 = False

    # H_4: G is the internal semidirect product of N and H
    try:
        if h1 and h2 and h3:
            if N.order() * H.order() == G.order():
                K = PermutationGroup(list(N.generators) + list(H.generators))
                h4 = (K.order() == G.order())
            else:
                h4 = False
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: H is not isomorphic to C_G(N) or G is not the internal direct product of N and C_G(N)
    try:
        if h1 and h2 and h3 and h4:
            c_elements = []
            N_gens = list(N.generators)
            for g in G.generate_dimino():
                if all(g * n == n * g for n in N_gens):
                    c_elements.append(g)
            
            # c_elements will always contain at least the identity element
            C = PermutationGroup(c_elements)
            
            is_iso = False
            if H.order() == C.order():
                try:
                    is_iso = H.is_isomorphic(C)
                except Exception:
                    # Fallback if is_isomorphic fails; if direct product holds, they must be isomorphic
                    is_iso = True
            
            is_direct_prod = False
            if N.order() * C.order() == G.order():
                K_C = PermutationGroup(list(N.generators) + list(C.generators))
                if K_C.order() == G.order():
                    is_direct_prod = True
                    
            neg_q = not (is_iso and is_direct_prod)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G, N, and H are permutation groups",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: G is the internal semidirect product of N and H",
    "¬Q: H is not isomorphic to C_G(N) or G is not the internal direct product of N and C_G(N)"
]

N_HYP = 4
NEG_Q_INDEX = 4