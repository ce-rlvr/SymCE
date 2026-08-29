import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def groups_equal(G1, G2):
    if not isinstance(G1, PermutationGroup) or not isinstance(G2, PermutationGroup):
        return False
    return G1.is_subgroup(G2) and G2.is_subgroup(G1)

def get_normalizer(G, H_elems):
    H_set = set(H_elems)
    n_elems = []
    for g in G.generate_dimino():
        try:
            if {g * h * ~g for h in H_set} == H_set:
                n_elems.append(g)
        except Exception:
            pass
    if not n_elems:
        n_elems.append(G.identity)
    return PermutationGroup(n_elems)

def get_centralizer(G, H_elems):
    c_elems = []
    for g in G.generate_dimino():
        try:
            if all(g * h * ~g == h for h in H_elems):
                c_elems.append(g)
        except Exception:
            pass
    if not c_elems:
        c_elems.append(G.identity)
    return PermutationGroup(c_elems)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            G, H = witness
            if isinstance(H, PermutationGroup):
                H_elems = list(H.generate_dimino())
            else:
                H_elems = list(H)
            N = get_normalizer(G, H_elems)
            C = get_centralizer(G, H_elems)
        elif len(witness) == 4:
            G, H, N, C = witness
            if isinstance(H, PermutationGroup):
                H_elems = list(H.generate_dimino())
            else:
                H_elems = list(H)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N_G(H) is the normalizer of H in G
    try:
        h_in_g = True
        g_elems = set(G.generate_dimino())
        for h in H_elems:
            if h not in g_elems:
                h_in_g = False
                break
        
        if not h_in_g:
            h2 = False
        else:
            true_N = get_normalizer(G, H_elems)
            h2 = groups_equal(N, true_N)
    except Exception:
        h2 = False

    # H3: C_G(H) is the centralizer of H in G
    try:
        true_C = get_centralizer(G, H_elems)
        h3 = groups_equal(C, true_C)
    except Exception:
        h3 = False

    # neg_Q: Conclusion fails
    try:
        c_is_normal = True
        try:
            if not C.is_subgroup(N):
                c_is_normal = False
            else:
                for n in N.generate_dimino():
                    for c in C.generate_dimino():
                        if n * c * ~n not in C:
                            c_is_normal = False
                            break
                    if not c_is_normal:
                        break
        except Exception:
            c_is_normal = False
        
        H_set = set(H_elems)
        is_group = True
        try:
            if G.identity not in H_set:
                is_group = False
            else:
                for a in H_set:
                    if ~a not in H_set:
                        is_group = False
                        break
                    for b in H_set:
                        if a * b not in H_set:
                            is_group = False
                            break
        except Exception:
            is_group = False
        
        if not is_group:
            q = False
        else:
            q = c_is_normal
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N_G(H) is the normalizer of H in G",
    "H_3: C_G(H) is the centralizer of H in G",
    "¬Q: C_G(H) is not a normal subgroup of N_G(H) or N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3