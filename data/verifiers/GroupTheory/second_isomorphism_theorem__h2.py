import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def get_elements(obj):
    if hasattr(obj, 'generate'):
        return set(obj.generate())
    return set(obj)

def eval_Q(G, N, H):
    try:
        G_elems = get_elements(G)
        N_elems = get_elements(N)
        H_elems = get_elements(H)
        
        if not H_elems:
            return False
            
        # Check if H is a group
        for h1 in H_elems:
            for h2 in H_elems:
                if h1 * h2 not in H_elems:
                    return False
            if h1**-1 not in H_elems:
                return False
                
        # Compute HN
        HN_elems = set()
        for h in H_elems:
            for n in N_elems:
                HN_elems.add(h * n)
                
        # Check if HN is a subgroup of G
        if not HN_elems.issubset(G_elems):
            return False
        for x in HN_elems:
            for y in HN_elems:
                if x * y not in HN_elems:
                    return False
            if x**-1 not in HN_elems:
                return False
                
        # H \cap N is a normal subgroup of H
        H_cap_N = H_elems.intersection(N_elems)
        if not H_cap_N:
            return False
        for x in H_cap_N:
            for y in H_cap_N:
                if x * y not in H_cap_N:
                    return False
            if x**-1 not in H_cap_N:
                return False
        for h in H_elems:
            for x in H_cap_N:
                if h * x * (h**-1) not in H_cap_N:
                    return False
                    
        # Check isomorphism condition (orders match for finite groups)
        if len(HN_elems) * len(H_cap_N) != len(H_elems) * len(N_elems):
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        G_elems = get_elements(G)
        if not G_elems:
            h1 = False
        else:
            h1 = True
            for x in G_elems:
                for y in G_elems:
                    if x * y not in G_elems:
                        h1 = False
                if x**-1 not in G_elems:
                    h1 = False
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        N_elems = get_elements(N)
        if not N_elems or not N_elems.issubset(G_elems):
            h2 = False
        else:
            is_group_N = True
            for x in N_elems:
                for y in N_elems:
                    if x * y not in N_elems:
                        is_group_N = False
                if x**-1 not in N_elems:
                    is_group_N = False
            if not is_group_N:
                h2 = False
            else:
                is_normal = True
                for g in G_elems:
                    for n in N_elems:
                        if g * n * (g**-1) not in N_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2 = is_normal
    except Exception:
        h2 = False

    # neg_Q: Q is false
    try:
        q_val = eval_Q(G, N, H)
        neg_q = not q_val
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: HN is not a subgroup of G, or H \\cap N is not a normal subgroup of H, or HN/N \\not\\cong H/(H \\cap N)"
]

N_HYP = 2
NEG_Q_INDEX = 2