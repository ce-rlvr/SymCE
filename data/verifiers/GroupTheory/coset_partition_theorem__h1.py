import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def to_list(obj):
    if hasattr(obj, 'elements'):
        return list(obj.elements)
    elif hasattr(obj, 'generate'):
        return list(obj.generate())
    else:
        return list(obj)

def get_unique(lst):
    unique = []
    for x in lst:
        if not any(x == y for y in unique):
            unique.append(x)
    return unique

def extract_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, H, op = witness
        elif len(witness) == 2:
            G, H = witness
            op = lambda x, y: x * y
        else:
            raise ValueError("Tuple witness must have 2 or 3 elements")
    elif isinstance(witness, dict):
        G = witness['G']
        H = witness['H']
        op = witness['op']
    else:
        G = witness.G
        H = witness.H
        op = witness.op
        
    G_list = to_list(G)
    H_list = to_list(H)
    return get_unique(G_list), get_unique(H_list), op

def is_subgroup(G, H, op):
    if not H:
        return False
        
    # H must be a subset of G
    for h in H:
        if not any(h == g for g in G):
            return False
            
    # H must be closed under op
    for h1 in H:
        for h2 in H:
            prod = op(h1, h2)
            if not any(prod == h for h in H):
                return False
                
    # Check associativity on H
    for h1 in H:
        for h2 in H:
            for h3 in H:
                if not (op(h1, op(h2, h3)) == op(op(h1, h2), h3)):
                    return False
                    
    # Find identity in H
    identities = []
    for e in H:
        is_id = True
        for h in H:
            if not (op(e, h) == h) or not (op(h, e) == h):
                is_id = False
                break
        if is_id:
            identities.append(e)
            
    if len(identities) != 1:
        return False
    e = identities[0]
    
    # Check inverses in H
    for h in H:
        has_inv = False
        for inv in H:
            if (op(h, inv) == e) and (op(inv, h) == e):
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def left_cosets_partition(G, H, op):
    cosets = []
    for g in G:
        coset = []
        for h in H:
            coset.append(op(g, h))
            
        unique_coset = []
        for x in coset:
            if not any(x == y for y in unique_coset):
                unique_coset.append(x)
                
        is_new = True
        for c in cosets:
            if len(c) == len(unique_coset):
                if all(any(x == y for y in c) for x in unique_coset):
                    is_new = False
                    break
        if is_new:
            cosets.append(unique_coset)
            
    union = []
    for c in cosets:
        for x in c:
            if not any(x == y for y in union):
                union.append(x)
                
    if len(union) != len(G):
        return False
        
    for x in union:
        if not any(x == g for g in G):
            return False
            
    for g in G:
        if not any(g == x for x in union):
            return False
            
    for i in range(len(cosets)):
        for j in range(i + 1, len(cosets)):
            c1 = cosets[i]
            c2 = cosets[j]
            for x in c1:
                if any(x == y for y in c2):
                    return False
                    
    return True

def conditions(witness):
    try:
        G, H, op = extract_witness(witness)
    except Exception:
        return [False, False]
        
    try:
        h1_ok = is_subgroup(G, H, op)
    except Exception:
        h1_ok = False
        
    try:
        q_ok = left_cosets_partition(G, H, op)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: The collection of all left cosets {gH | g \in G} does not form a partition of G"
]

N_HYP = 1
NEG_Q_INDEX = 1