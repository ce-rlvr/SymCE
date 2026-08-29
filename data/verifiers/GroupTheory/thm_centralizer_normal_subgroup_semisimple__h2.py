import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, N, M = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = all(n in G for n in N.generators)
        if h2:
            is_normal = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            h2 = is_normal
    except Exception:
        h2 = False

    # H_3: M is the normal complement of N in G, meaning G is the internal direct product of N and M
    try:
        h3_1 = all(m in G for m in M.generators)
        if h3_1:
            is_normal_M = True
            for g in G.generators:
                for m in M.generators:
                    if (g * m * ~g) not in M:
                        is_normal_M = False
                        break
                if not is_normal_M:
                    break
            
            N_M_gens = list(N.generators) + list(M.generators)
            if not N_M_gens:
                N_M = PermutationGroup([G.identity])
            else:
                N_M = PermutationGroup(N_M_gens)
            
            # Internal direct product requires N and M to be normal, N intersect M = {1}, and NM = G.
            # Since N and M are normal, NM is a subgroup. |NM| = |N|*|M| / |N intersect M|.
            # Thus |NM| == |G| and |N|*|M| == |G| implies |N intersect M| == 1 and NM = G.
            h3 = is_normal_M and (N.order() * M.order() == G.order()) and (N_M.order() == G.order())
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The centralizer C_G(N) is not equal to M
    try:
        if G.order() > 2000:
            neg_q = False
        else:
            c_g_n_equals_m = True
            c_g_n_size = 0
            for g in G.generate():
                commutes = True
                for n in N.generators:
                    if g * n != n * g:
                        commutes = False
                        break
                if commutes:
                    c_g_n_size += 1
                    if g not in M:
                        c_g_n_equals_m = False
                        break
            
            if c_g_n_equals_m:
                if c_g_n_size != M.order():
                    c_g_n_equals_m = False
                    
            neg_q = not c_g_n_equals_m
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: M is the normal complement of N in G",
    "¬Q: The centralizer C_G(N) is not equal to M"
]

N_HYP = 3
NEG_Q_INDEX = 3