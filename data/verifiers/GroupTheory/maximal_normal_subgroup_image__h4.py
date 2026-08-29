import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, f, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: f: G -> H is a surjective group homomorphism
    try:
        G_elems = list(G.generate_dimino())
        H_elems = list(H.generate_dimino())
        
        if callable(f):
            f_dict = {g: f(g) for g in G_elems}
        elif isinstance(f, dict):
            f_dict = f
        else:
            f_dict = None
            
        if f_dict is None:
            h2 = False
        else:
            if set(f_dict.keys()) != set(G_elems):
                h2 = False
            elif not set(f_dict.values()).issubset(set(H_elems)):
                h2 = False
            elif set(f_dict.values()) != set(H_elems):
                h2 = False
            else:
                h2 = True
                for x in G_elems:
                    for y in G_elems:
                        if f_dict[x * y] != f_dict[x] * f_dict[y]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: N is a maximal normal subgroup of G
    try:
        if isinstance(N, PermutationGroup):
            N_elems = set(N.generate_dimino())
        else:
            N_elems = set(N)
            
        G_elems_set = set(G.generate_dimino())
        
        if not N_elems.issubset(G_elems_set):
            h3 = False
        elif N_elems == G_elems_set:
            h3 = False
        else:
            is_normal = True
            if G.identity not in N_elems:
                is_normal = False
            else:
                for n1 in N_elems:
                    for n2 in N_elems:
                        if n1 * n2 not in N_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                if is_normal:
                    for n in N_elems:
                        if ~n not in N_elems:
                            is_normal = False
                            break
            if is_normal:
                for g in G_elems_set:
                    for n in N_elems:
                        if g * n * ~g not in N_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            if not is_normal:
                h3 = False
            else:
                normal_subs = G.normal_subgroups()
                h3 = True
                for ns in normal_subs:
                    ns_elems = set(ns.generate_dimino())
                    if ns_elems != G_elems_set and ns_elems != N_elems:
                        if N_elems.issubset(ns_elems):
                            h3 = False
                            break
    except Exception:
        h3 = False

    # neg_Q: f(N) is NOT a maximal normal subgroup of H
    try:
        if callable(f):
            f_dict = {g: f(g) for g in G.generate_dimino()}
        else:
            f_dict = f
            
        if isinstance(N, PermutationGroup):
            N_elems = set(N.generate_dimino())
        else:
            N_elems = set(N)
            
        fN_elems = {f_dict[n] for n in N_elems}
        H_elems_set = set(H.generate_dimino())
        
        is_fN_maximal_normal = True
        
        if not fN_elems.issubset(H_elems_set):
            is_fN_maximal_normal = False
        elif fN_elems == H_elems_set:
            is_fN_maximal_normal = False
        else:
            is_normal = True
            if H.identity not in fN_elems:
                is_normal = False
            else:
                for n1 in fN_elems:
                    for n2 in fN_elems:
                        if n1 * n2 not in fN_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                if is_normal:
                    for n in fN_elems:
                        if ~n not in fN_elems:
                            is_normal = False
                            break
            if is_normal:
                for h in H_elems_set:
                    for n in fN_elems:
                        if h * n * ~h not in fN_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            if not is_normal:
                is_fN_maximal_normal = False
            else:
                normal_subs_H = H.normal_subgroups()
                for ns in normal_subs_H:
                    ns_elems = set(ns.generate_dimino())
                    if ns_elems != H_elems_set and ns_elems != fN_elems:
                        if fN_elems.issubset(ns_elems):
                            is_fN_maximal_normal = False
                            break
                            
        neg_q = not is_fN_maximal_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a surjective group homomorphism",
    "H_3: N is a maximal normal subgroup of G",
    "¬Q: f(N) is not a maximal normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3