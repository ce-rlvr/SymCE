import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
from itertools import combinations

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
# V4 as the Klein 4-group (a standard counterexample for this theorem)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_normal_subgroups(G):
    elements = list(G.elements)
    classes = []
    seen = set()
    for g in elements:
        if g in seen:
            continue
        c = set()
        for x in elements:
            c.add(x * g * ~x)
        classes.append(c)
        seen.update(c)
    
    id_class = None
    other_classes = []
    for c in classes:
        if any(g.is_Identity for g in c):
            id_class = c
        else:
            other_classes.append(c)
            
    valid_combos = []
    n_classes = len(other_classes)
    order_G = G.order()
    
    def search(index, current_combo, current_size):
        if order_G % current_size == 0:
            valid_combos.append(current_combo)
        
        for i in range(index, n_classes):
            c = other_classes[i]
            search(i + 1, current_combo + [c], current_size + len(c))

    search(0, [], len(id_class))
    
    normal_subgroups = []
    for combo in valid_combos:
        union = set(id_class)
        for c in combo:
            union.update(c)
            
        is_subgroup = True
        for a in union:
            for b in union:
                if a * b not in union:
                    is_subgroup = False
                    break
            if not is_subgroup:
                break
        if is_subgroup:
            normal_subgroups.append(union)
            
    return normal_subgroups

def is_semisimple(G, normals):
    # A finite group is semisimple (a direct product of simple groups) 
    # iff every normal subgroup has a normal complement.
    if G.order() == 1:
        return False
    for N in normals:
        has_complement = False
        for M in normals:
            if len(N.intersection(M)) == 1:
                if len(N) * len(M) == G.order():
                    has_complement = True
                    break
        if not has_complement:
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, k = witness
        else:
            G = witness
            k = None
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(G, PermutationGroup):
            normals = get_normal_subgroups(G)
        else:
            normals = None
    except Exception:
        normals = None

    # H1: G is a finite semisimple group
    try:
        if normals is None:
            h1 = False
        else:
            h1 = is_semisimple(G, normals)
    except Exception:
        h1 = False
        
    # H2: k is a positive integer
    try:
        h2 = isinstance(k, int) and k > 0
    except Exception:
        h2 = False
        
    # neg_Q: G does NOT have exactly 2^k distinct normal subgroups
    try:
        if normals is None or not isinstance(k, int) or k < 0:
            neg_q = False
        else:
            neg_q = len(normals) != (2 ** k)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "H_2: k is a positive integer",
    "¬Q: G does not have exactly 2^k distinct normal subgroups"
]

N_HYP = 2
NEG_Q_INDEX = 2