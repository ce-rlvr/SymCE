import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

# Top-level setup
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

def are_groups_equal(H1, H2):
    if H1.order() != H2.order():
        return False
    for g in H1.generators:
        if g not in H2:
            return False
    return True

def get_all_sylows(G, p):
    P0 = G.sylow_subgroup(p)
    sylows = [P0]
    queue = [P0]
    G_gens = G.generators
    if not G_gens:
        return sylows
    while queue:
        curr = queue.pop(0)
        for g in G_gens:
            if not curr.generators:
                H = P0
            else:
                conj_gens = [~g * gen * g for gen in curr.generators]
                H = PermutationGroup(conj_gens)
            is_new = True
            for S in sylows:
                if are_groups_equal(H, S):
                    is_new = False
                    break
            if is_new:
                sylows.append(H)
                queue.append(H)
    return sylows

def conditions(witness):
    try:
        G, p, P, S = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime dividing the order of G
    try:
        h2 = isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        else:
            order_G = G.order()
            order_P = P.order()
            expected_order = 1
            temp = order_G
            while temp % p == 0:
                expected_order *= p
                temp //= p
            
            if order_P != expected_order:
                h3 = False
            else:
                h3 = all(gen in G for gen in P.generators)
    except Exception:
        h3 = False

    # H4: S is the set of all Sylow p-subgroups of G
    try:
        if not isinstance(S, (list, set, tuple)):
            h4 = False
        else:
            all_sylows = get_all_sylows(G, p)
            if len(S) != len(all_sylows):
                h4 = False
            else:
                h4 = True
                for s_grp in S:
                    if not isinstance(s_grp, PermutationGroup):
                        h4 = False
                        break
                    match = False
                    for true_s in all_sylows:
                        if are_groups_equal(s_grp, true_s):
                            match = True
                            break
                    if not match:
                        h4 = False
                        break
                
                if h4:
                    for true_s in all_sylows:
                        match = False
                        for s_grp in S:
                            if are_groups_equal(s_grp, true_s):
                                match = True
                                break
                        if not match:
                            h4 = False
                            break
    except Exception:
        h4 = False

    # neg_Q: The number of Sylow p-subgroups of G (the cardinality of S) is NOT congruent to 1 modulo p
    try:
        neg_q = (len(S) % p) != 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: S is the set of all Sylow p-subgroups of G",
    "¬Q: The number of Sylow p-subgroups of G (the cardinality of S) is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4