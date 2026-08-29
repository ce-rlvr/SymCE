import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import itertools
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_identity(elements):
    for g in elements:
        if g * g == g:
            return g
    return None

def get_normal_subgroups(G, elements):
    classes = []
    seen = set()
    id_elem = get_identity(elements)
    for g in elements:
        if g not in seen:
            c = set()
            for x in elements:
                c.add(x * g * ~x)
            classes.append(list(c))
            seen.update(c)
    
    id_class = None
    other_classes = []
    for c in classes:
        if id_elem in c:
            id_class = c
        else:
            other_classes.append(c)
            
    normal_subgroups = []
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

def find_frobenius_kernel(G, elements):
    normal_subgroups = get_normal_subgroups(G, elements)
    id_elem = get_identity(elements)
    for N in normal_subgroups:
        if len(N) > 1 and len(N) < len(elements):
            is_kernel = True
            for n in N:
                if n == id_elem:
                    continue
                for x in elements:
                    if x * n == n * x:
                        if x not in N:
                            is_kernel = False
                            break
                if not is_kernel:
                    break
            if is_kernel:
                return N
    return None

def check_internal_sdp(G, K, H):
    G_elems = set(G.generate())
    K_elems = set(K.generate())
    H_elems = set(H.generate())
    
    if not K_elems.issubset(G_elems): 
        return False
    if not H_elems.issubset(G_elems): 
        return False
    
    for g in G_elems:
        for k in K_elems:
            if g * k * ~g not in K_elems:
                return False
                
    id_elem = get_identity(G_elems)
    intersection = K_elems.intersection(H_elems)
    if intersection != {id_elem}:
        return False
        
    if len(K_elems) * len(H_elems) != len(G_elems):
        return False
        
    return True

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, K, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        G_elems = list(G.generate())
        kernel_elems = find_frobenius_kernel(G, G_elems)
        h1 = (kernel_elems is not None)
    except Exception:
        h1 = False

    try:
        if kernel_elems is not None:
            K_elems = set(K.generate())
            h2 = (K_elems == set(kernel_elems))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        q = check_internal_sdp(G, K, H)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite Frobenius group",
    "H_2: K is the Frobenius kernel of G",
    "¬Q: G is not isomorphic to the internal semidirect product K ⋊ H"
]

N_HYP = 2
NEG_Q_INDEX = 2