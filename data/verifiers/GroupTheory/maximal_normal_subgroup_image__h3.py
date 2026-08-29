import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_identity(group):
    if hasattr(group, 'identity'):
        return group.identity
    elements = list(group.elements)
    for g in elements:
        if all(g * h == h for h in elements):
            return g
    return None

def get_all_normal_subgroups(group):
    classes = []
    seen = set()
    elements = list(group.elements)
    for g in elements:
        if g not in seen:
            c = frozenset(h * g * h**-1 for h in elements)
            classes.append(c)
            seen.update(c)
    
    normal_subgroups = []
    identity = get_identity(group)
    id_class = frozenset([identity])
    other_classes = [c for c in classes if c != id_class]
    
    for r in range(len(other_classes) + 1):
        for combo in itertools.combinations(other_classes, r):
            subset = set(id_class)
            for c in combo:
                subset.update(c)
            
            is_subgroup = True
            for a in subset:
                for b in subset:
                    if a * b not in subset:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                normal_subgroups.append(subset)
    return normal_subgroups

def is_maximal_normal_subgroup(elements_set, group):
    normal_subgroups = get_all_normal_subgroups(group)
    group_order = len(list(group.elements))
    if elements_set not in normal_subgroups:
        return False
    if len(elements_set) == group_order:
        return False
    for K_elems in normal_subgroups:
        if K_elems != elements_set and len(K_elems) != group_order:
            if elements_set.issubset(K_elems):
                return False
    return True

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

    # H2: f is a surjective group homomorphism from G to H
    try:
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
            
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        
        h2 = True
        mapped_elements = set()
        for g in G_elems:
            val = f_func(g)
            if val not in H_elems:
                h2 = False
                break
            mapped_elements.add(val)
            
        if h2:
            if mapped_elements != set(H_elems):
                h2 = False
                
        if h2:
            for g1 in G_elems:
                for g2 in G_elems:
                    if f_func(g1 * g2) != f_func(g1) * f_func(g2):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: ker(f) is a subset of N
    try:
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
            
        identity = get_identity(H)
        ker_f = set(g for g in G.elements if f_func(g) == identity)
        N_set = set(N)
        h3 = ker_f.issubset(N_set) and N_set.issubset(set(G.elements))
    except Exception:
        h3 = False

    # neg_Q: f(N) is NOT a maximal normal subgroup of H
    try:
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
            
        f_N = set(f_func(n) for n in N)
        neg_q = not is_maximal_normal_subgroup(f_N, H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism from G to H",
    "H_3: ker(f) is a subset of N",
    "¬Q: f(N) is not a maximal normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3