import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from itertools import combinations

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

def get_order(H):
    if callable(H.order):
        return H.order()
    return H.order

def check_solvable(G):
    if callable(G.is_solvable):
        return G.is_solvable()
    return G.is_solvable

def comb(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c

def has_subgroup_of_order(G, m):
    if m == 1:
        return True
    
    order = get_order(G)
        
    if m == order:
        return True
    if order % m != 0:
        return False
        
    if order > 2000:
        return False
        
    elements = list(G.elements)
    
    id_el = None
    for e in elements:
        if e * e == e:
            id_el = e
            break
            
    # Check 1-generator subgroups
    for e in elements:
        if get_order(PermutationGroup([e])) == m:
            return True
            
    # Check 2-generator subgroups
    for e1, e2 in combinations(elements, 2):
        if get_order(PermutationGroup([e1, e2])) == m:
            return True
            
    # Check 3-generator subgroups for small groups
    if len(elements) <= 24:
        for e1, e2, e3 in combinations(elements, 3):
            if get_order(PermutationGroup([e1, e2, e3])) == m:
                return True
                
    # Exhaustive subset check for small combinations
    others = [e for e in elements if e != id_el]
    if comb(len(others), m - 1) < 5000:
        for subset in combinations(others, m - 1):
            subset_set = set(subset)
            subset_set.add(id_el)
            
            is_subgroup = True
            for a in subset:
                if a**2 not in subset_set:
                    is_subgroup = False
                    break
            if not is_subgroup:
                continue
                
            for a, b in combinations(subset, 2):
                if a * b not in subset_set:
                    is_subgroup = False
                    break
                if b * a not in subset_set:
                    is_subgroup = False
                    break
                    
            if is_subgroup:
                return True
                
    return False

def conditions(witness):
    try:
        G, m, n = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group and m, n are positive integers
    try:
        m_val = int(m)
        n_val = int(n)
        h1 = (isinstance(G, PermutationGroup) and 
              m_val == m and n_val == n and 
              m_val > 0 and n_val > 0)
        m = m_val
        n = n_val
    except Exception:
        h1 = False
        
    # H_2: G is a solvable group
    try:
        h2 = bool(check_solvable(G))
    except Exception:
        h2 = False
        
    # H_3: The order of G is m * n
    try:
        h3 = bool(get_order(G) == m * n)
    except Exception:
        h3 = False
        
    # ¬Q: G does not contain a subgroup of order m
    try:
        neg_q = not has_subgroup_of_order(G, m)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and m, n are positive integers",
    "H_2: G is a solvable group",
    "H_3: The order of G is m * n",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3