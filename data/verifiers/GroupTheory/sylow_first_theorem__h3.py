import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for potential witness expressions
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

def has_subgroup_of_order(G, k):
    """
    Helper function to determine if a PermutationGroup G has a subgroup of order k.
    Uses a BFS approach to generate subgroups.
    """
    if k == 1 or k == G.order():
        return True
    if G.order() % k != 0:
        return False
        
    elements = list(G.generate())
    if not elements:
        return False
        
    id_elem = elements[0]**0
        
    # subgroups stores frozensets of elements to avoid redundant exploration
    subgroups = {frozenset([id_elem])}
    # queue stores tuples of (list_of_generators, frozenset_of_elements)
    queue = [([], frozenset([id_elem]))]
    
    while queue:
        curr_gens, curr_elems = queue.pop(0)
        
        for g in elements:
            if g not in curr_elems:
                new_gens = curr_gens + [g]
                new_group = PermutationGroup(*new_gens)
                new_order = new_group.order()
                
                if new_order == k:
                    return True
                    
                if new_order < G.order():
                    new_elems = frozenset(new_group.generate())
                    if new_elems not in subgroups:
                        subgroups.add(new_elems)
                        queue.append((new_gens, new_elems))
                        
    return False

def conditions(witness) -> list[bool]:
    try:
        G, p, n, m = witness
    except Exception:
        return [False] * 5
        
    # H_1: G is a finite group
    try:
        order_G = G.order()
        h1 = isinstance(order_G, (int, sympy.Integer)) and order_G > 0
    except Exception:
        h1 = False
        
    # H_2: The order of G is p^n * m
    try:
        h2 = (isinstance(p, (int, sympy.Integer)) and 
              isinstance(m, (int, sympy.Integer)) and 
              int(order_G) == (int(p)**int(n)) * int(m))
    except Exception:
        h2 = False
        
    # H_3: n is an integer greater than or equal to 1
    try:
        h3 = isinstance(n, (int, sympy.Integer)) and int(n) >= 1
    except Exception:
        h3 = False
        
    # H_4: p does not divide m
    try:
        h4 = int(m) % int(p) != 0
    except Exception:
        h4 = False
        
    # ¬Q: G does NOT contain a subgroup of order p^n
    try:
        k = int(p)**int(n)
        neg_q = not has_subgroup_of_order(G, k)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p^n * m",
    "H_3: n is an integer greater than or equal to 1",
    "H_4: p does not divide m",
    "¬Q: G does not contain a subgroup of order p^n"
]

N_HYP = 4
NEG_Q_INDEX = 4