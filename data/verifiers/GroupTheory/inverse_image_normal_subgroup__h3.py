import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            M = witness.get('M')
        else:
            G, H, f, M = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: f: G \to H is a group homomorphism
    try:
        h2 = True
        if not h1:
            h2 = False
        else:
            elements_G = list(G.elements)
            elements_H = list(H.elements)
            
            f_map = {}
            if callable(f):
                for g in elements_G:
                    f_map[g] = f(g)
            elif isinstance(f, dict):
                f_map = f
            else:
                h2 = False
                
            if h2:
                for g in elements_G:
                    if g not in f_map or f_map[g] not in elements_H:
                        h2 = False
                        break
            if h2:
                for x in elements_G:
                    for y in elements_G:
                        if f_map[x * y] != f_map[x] * f_map[y]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: The preimage f^{-1}(M) is NOT a normal subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            if isinstance(M, PermutationGroup):
                M_elements = set(M.elements)
            else:
                M_elements = set(M)
                
            elements_G = list(G.elements)
            f_map_q = {}
            if callable(f):
                for g in elements_G:
                    f_map_q[g] = f(g)
            elif isinstance(f, dict):
                f_map_q = f
            else:
                f_map_q = {}
                
            preimage = [g for g in elements_G if g in f_map_q and f_map_q[g] in M_elements]
            preimage_set = set(preimage)
            
            is_subgroup = True
            if not preimage:
                is_subgroup = False
            elif G.identity not in preimage_set:
                is_subgroup = False
            else:
                for x in preimage:
                    for y in preimage:
                        if x * y not in preimage_set:
                            is_subgroup = False
                            break
                    if x**-1 not in preimage_set:
                        is_subgroup = False
                    if not is_subgroup:
                        break
                        
            is_normal = True
            if is_subgroup:
                for g in elements_G:
                    for n in preimage:
                        if g * n * g**-1 not in preimage_set:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            else:
                is_normal = False
                
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: f^{-1}(M) is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2