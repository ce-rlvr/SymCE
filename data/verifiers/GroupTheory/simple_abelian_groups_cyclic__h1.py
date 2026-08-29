import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_simple_group(G):
    """
    Checks if a permutation group G is simple.
    A group is simple if its only normal subgroups are the trivial group and itself.
    """
    if not isinstance(G, PermutationGroup):
        return False
        
    # If sympy ever adds an is_simple property, use it
    if hasattr(G, 'is_simple'):
        res = G.is_simple
        if callable(res):
            return res()
        elif res is not None:
            return res

    order = G.order()
    if order == 1:
        return False
    if isprime(order):
        return True
        
    # If G is not perfect, its derived subgroup is a proper normal subgroup.
    D = G.derived_subgroup()
    if D.order() < order:
        return False
        
    # If G is perfect but has a non-trivial center, the center is a proper normal subgroup.
    C = G.center()
    if C.order() > 1:
        return False
        
    # For perfect groups with trivial center, we find all conjugacy classes.
    elements = list(G.elements)
    classes = []
    unseen = set(elements)
    gens = G.generators
    
    while unseen:
        x = unseen.pop()
        cclass = {x}
        queue = [x]
        # The conjugacy class is the orbit of x under conjugation by the generators
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = g * curr * ~g
                if nxt not in cclass:
                    cclass.add(nxt)
                    queue.append(nxt)
        classes.append(cclass)
        unseen -= cclass
        
    id_class = None
    other_classes = []
    for c in classes:
        if len(c) == 1:
            id_class = c
        else:
            other_classes.append(c)
            
    # A normal subgroup is a union of conjugacy classes that includes the identity.
    # We check all possible unions of classes to see if their size divides the order of G.
    for r in range(1, len(other_classes)):
        for combo in combinations(other_classes, r):
            size = 1 + sum(len(c) for c in combo)
            if order % size == 0:
                subset = set(id_class)
                for c in combo:
                    subset.update(c)
                
                # Check if the subset is closed under multiplication (i.e., it is a subgroup)
                is_subgroup = True
                for x in subset:
                    for y in subset:
                        if x * y not in subset:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                if is_subgroup:
                    return False
                    
    return True

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False]
            
        is_simple = is_simple_group(witness)
        is_prime_cyclic = isprime(witness.order())
        
        # The conclusion is: G is simple <-> G is prime cyclic
        # The negated conclusion is True when this equivalence fails (i.e., XOR)
        neg_q = bool(is_simple != is_prime_cyclic)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: G is a simple group but is not isomorphic to a cyclic group of prime order (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0