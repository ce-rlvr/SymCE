import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def is_subgroup(sub, G):
    return set(sub.elements).issubset(set(G.elements))

def is_complement(G, N, H):
    N_elems = set(N.elements)
    H_elems = set(H.elements)
    G_elems = set(G.elements)
    if len(N_elems) * len(H_elems) != len(G_elems):
        return False
    if len(N_elems.intersection(H_elems)) != 1:
        return False
    return True

def transfer(G, H, g):
    reps = []
    seen = set()
    H_elems = list(H.elements)
    H_set = set(H_elems)
    
    # Find left coset representatives
    for x in G.elements:
        if x not in seen:
            reps.append(x)
            for h in H_elems:
                seen.add(x * h)
                
    res = None
    for x in reps:
        gx = g * x
        for xj in reps:
            h = xj**-1 * gx
            if h in H_set:
                if res is None:
                    res = h
                else:
                    res = res * h
                break
                
    if res is None:
        for e in G.elements:
            if e * e == e:
                return e
    return res

def conclusion(G, N, H):
    N_elems = list(N.elements)
    H_elems = list(H.elements)
    N_len = len(N_elems)
    
    identity = None
    for e in G.elements:
        if e * e == e:
            identity = e
            break
            
    # Check V(h) == h^{|N|} for all h in H
    for h in H_elems:
        vh = transfer(G, H, h)
        expected = h**N_len
        if vh != expected:
            return False
            
    # Check N is contained in ker(V)
    for n in N_elems:
        vn = transfer(G, H, n)
        if vn != identity:
            return False
            
    return True

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_subgroup(N, G) and is_subgroup(H, G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_complement(G, N, H)
    except Exception:
        h2 = False
        
    try:
        h3 = bool(H.is_abelian)
    except Exception:
        h3 = False
        
    try:
        neg_q = not conclusion(G, N, H)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are subgroups of G",
    "H_2: H is a complement of N in G",
    "H_3: H is abelian",
    "¬Q: The restriction of V to H is not V(h) = h^{|N|} or N is not contained in ker(V)"
]

N_HYP = 3
NEG_Q_INDEX = 3