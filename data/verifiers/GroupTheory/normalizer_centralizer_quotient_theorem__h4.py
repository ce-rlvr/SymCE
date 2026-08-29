import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_normalizer(G, H):
    norm_elements = []
    H_elems = set(H.elements)
    for g in G.elements:
        if all((g * h * ~g) in H_elems for h in H.generators):
            norm_elements.append(g)
    return PermutationGroup(norm_elements)

def get_centralizer(G, H):
    cent_elements = []
    for g in G.elements:
        if all((g * h * ~g) == h for h in H.generators):
            cent_elements.append(g)
    return PermutationGroup(cent_elements)

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        G = witness[0] if len(witness) > 0 else None
        H = witness[1] if len(witness) > 1 else None
        N = witness[2] if len(witness) > 2 else None
    else:
        G = witness
        H = None
        N = None

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: N_G(H) is the normalizer of H in G
    try:
        if h1 and h2:
            N_actual = get_normalizer(G, H)
            if N is not None:
                h3 = isinstance(N, PermutationGroup) and set(N.elements) == set(N_actual.elements)
            else:
                N = N_actual
                h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # Conclusion: C_G(H) is a normal subgroup of N_G(H), and N_G(H)/C_G(H) is isomorphic to a subgroup of Aut(H)
    try:
        if h1 and h2 and h3:
            C_actual = get_centralizer(G, H)
            C_actual_elems = set(C_actual.elements)
            N_elems = set(N.elements)
            
            # Check if C_G(H) is a subgroup of N_G(H)
            is_subgroup_actual = C_actual_elems.issubset(N_elems)
            
            # Check if C_G(H) is a normal subgroup of N_G(H)
            is_normal_actual = True
            if is_subgroup_actual:
                for n in N_elems:
                    for c in C_actual_elems:
                        if (n * c * ~n) not in C_actual_elems:
                            is_normal_actual = False
                            break
                    if not is_normal_actual:
                        break
            else:
                is_normal_actual = False
                
            # Check if N_G(H)/C_G(H) is isomorphic to a subgroup of Aut(H)
            # We compute the number of distinct automorphisms of H induced by conjugation by elements of N_G(H).
            # This forms a subgroup of Aut(H) isomorphic to N_G(H)/C_G(H).
            automorphisms = set()
            H_list = list(H.elements)
            for n in N_elems:
                mapping = tuple(H_list.index(n * h * ~n) for h in H_list)
                automorphisms.add(mapping)
            
            quotient_size = len(N_elems) // len(C_actual_elems)
            is_isomorphic = (len(automorphisms) == quotient_size)
            
            Q = is_normal_actual and is_isomorphic
            neg_Q = not Q
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N_G(H) is the normalizer of H in G",
    "¬Q: C_G(H) is not a normal subgroup of N_G(H) or N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3