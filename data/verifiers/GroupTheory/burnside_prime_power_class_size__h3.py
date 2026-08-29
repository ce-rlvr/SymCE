import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_simple(G):
    """Helper function to check if a finite permutation group is simple."""
    order = G.order()
    if order <= 1:
        return False
    if isprime(order):
        return True
    
    try:
        elements = list(G.elements)
    except Exception:
        elements = list(G.generate_dimino())
        
    generators = G.generators
    seen = set()
    classes = []
    
    # Compute conjugacy classes efficiently using generators
    for g in elements:
        if g in seen:
            continue
        cclass = {g}
        queue = [g]
        while queue:
            curr = queue.pop(0)
            for gen in generators:
                nxt1 = gen * curr * ~gen
                if nxt1 not in cclass:
                    cclass.add(nxt1)
                    queue.append(nxt1)
                nxt2 = ~gen * curr * gen
                if nxt2 not in cclass:
                    cclass.add(nxt2)
                    queue.append(nxt2)
        seen.update(cclass)
        classes.append(cclass)
    
    # Find the identity element
    identity = None
    for g in elements:
        if g * g == g:
            identity = g
            break
            
    id_class = None
    other_classes = []
    for c in classes:
        if identity in c:
            id_class = c
        else:
            other_classes.append(c)
            
    divisors = [d for d in range(2, order) if order % d == 0]
    target_sizes = {d - 1 for d in divisors}
    max_target = max(target_sizes) if target_sizes else 0
    
    # Sort classes by size descending for faster pruning
    other_classes.sort(key=len, reverse=True)
    
    # Backtracking to find if any union of conjugacy classes forms a proper normal subgroup
    def find_subgroups(index, current_subset, current_sum):
        if current_sum in target_sizes:
            union = set(id_class)
            for c in current_subset:
                union.update(c)
            is_subgroup = True
            union_list = list(union)
            # Check closure under multiplication
            for a in union_list:
                for b in union_list:
                    if a * b not in union:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                return True
                
        if index == len(other_classes):
            return False
            
        if current_sum > max_target:
            return False
            
        # Include the current conjugacy class
        c = other_classes[index]
        current_subset.append(c)
        if find_subgroups(index + 1, current_subset, current_sum + len(c)):
            return True
        current_subset.pop()
        
        # Exclude the current conjugacy class
        if find_subgroups(index + 1, current_subset, current_sum):
            return True
            
        return False

    if find_subgroups(0, [], 0):
        return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, p, k = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: k > 0
    try:
        h3 = k > 0 and int(k) == k
    except Exception:
        h3 = False

    # ¬Q: G is a simple group (negation of "G is not a simple group")
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = is_simple(G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: k > 0",
    "¬Q: G is a simple group"
]

N_HYP = 3
NEG_Q_INDEX = 3