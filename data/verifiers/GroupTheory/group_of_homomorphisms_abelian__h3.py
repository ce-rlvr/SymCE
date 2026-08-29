import itertools
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
)
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

def get_homomorphisms(G, A):
    gens = list(G.generators)
    homs = []
    G_elems = list(G.elements)
    A_elems = list(A.elements)
    for target in itertools.product(A_elems, repeat=len(gens)):
        mapping = {G.identity: A.identity}
        for g, t in zip(gens, target):
            mapping[g] = t
        
        queue = [G.identity]
        valid = True
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                nxt_val = mapping[curr] * mapping[g]
                if nxt in mapping:
                    if mapping[nxt] != nxt_val:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_val
                    queue.append(nxt)
            if not valid:
                break
        if valid and len(mapping) == len(G_elems):
            is_hom = True
            for x in G_elems:
                for y in G_elems:
                    if mapping[x * y] != mapping[x] * mapping[y]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            if is_hom:
                homs.append(mapping)
    return homs

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, A = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if isinstance(A, PermutationGroup) and hasattr(A, 'is_abelian'):
            val = A.is_abelian
            if callable(val):
                h2 = bool(val())
            else:
                h2 = bool(val)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        homs = get_homomorphisms(G, A)
        
        is_group = True
        is_abelian = True
        
        G_elems = list(G.elements)
        
        hom_tuples = set()
        for f in homs:
            hom_tuples.add(tuple(f[x] for x in G_elems))
            
        id_tuple = tuple(A.identity for _ in G_elems)
        if id_tuple not in hom_tuples:
            is_group = False
            
        for f in homs:
            if not is_group and not is_abelian:
                break
            for g in homs:
                fg_tuple = tuple(f[x] * g[x] for x in G_elems)
                if fg_tuple not in hom_tuples:
                    is_group = False
                
                gf_tuple = tuple(g[x] * f[x] for x in G_elems)
                if fg_tuple != gf_tuple:
                    is_abelian = False
                    
        if is_group:
            for f in homs:
                has_inv = False
                for g in homs:
                    fg_tuple = tuple(f[x] * g[x] for x in G_elems)
                    gf_tuple = tuple(g[x] * f[x] for x in G_elems)
                    if fg_tuple == id_tuple and gf_tuple == id_tuple:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break
                    
        neg_q = not (is_group and is_abelian)
        
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A is an abelian group",
    "¬Q: Hom(G, A) does not form an abelian group under pointwise operation"
]
N_HYP = 2
NEG_Q_INDEX = 2