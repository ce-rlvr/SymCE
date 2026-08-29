import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

try:
    V4 = Z2 * Z2
except Exception:
    V4 = DihedralGroup(2)

def direct_product(G, H):
    try:
        return G * H
    except Exception:
        pass
    
    degG = G.degree
    degH = H.degree
    if degG == 0: degG = 1
    if degH == 0: degH = 1
    
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degG:
            arr += list(range(len(arr), degG))
        arr += list(range(degG, degG + degH))
        gens.append(Permutation(arr))
    for h in H.generators:
        arr = list(range(degG))
        h_arr = list(h.array_form)
        if len(h_arr) < degH:
            h_arr += list(range(len(h_arr), degH))
        arr += [x + degG for x in h_arr]
        gens.append(Permutation(arr))
        
    if not gens:
        return PermutationGroup([Permutation()])
    return PermutationGroup(gens)

def is_subdirectly_irreducible(grp):
    try:
        if grp.order() <= 1:
            return False
        
        elements = list(grp.generate())
        classes = []
        seen = set()
        for g in elements:
            if g in seen:
                continue
            cclass = set()
            for x in elements:
                cclass.add(x * g * ~x)
            classes.append(cclass)
            seen.update(cclass)
            
        normal_subgroups = []
        for cclass in classes:
            c_list = list(cclass)
            if all(g.is_Identity for g in c_list):
                continue
            H = PermutationGroup(c_list)
            H_els = frozenset(H.generate())
            normal_subgroups.append(H_els)
            
        if not normal_subgroups:
            return False
            
        minimal_normals = set()
        for N in normal_subgroups:
            is_minimal = True
            for M in normal_subgroups:
                if M != N and M.issubset(N):
                    is_minimal = False
                    break
            if is_minimal:
                minimal_normals.add(N)
                
        return len(minimal_normals) == 1
    except Exception:
        return False

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G is non-trivial
    try:
        h2 = h1 and G.order() > 1
    except Exception:
        h2 = False
        
    # ¬Q: G x H is subdirectly irreducible
    try:
        if not h1:
            neg_q = False
        else:
            GxH = direct_product(G, H)
            neg_q = is_subdirectly_irreducible(GxH)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is non-trivial",
    "¬Q: G x H is subdirectly irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2