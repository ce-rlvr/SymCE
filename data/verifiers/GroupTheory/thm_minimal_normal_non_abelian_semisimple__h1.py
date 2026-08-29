import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
S6 = SymmetricGroup(6)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
A6 = AlternatingGroup(6)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def is_semisimple(G):
    """
    A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    Equivalently, the normal closure of every non-identity element is non-abelian.
    """
    if G.order() == 1:
        return True
        
    elements = list(G.generate())
    unvisited = set(elements)
    for g in elements:
        if g.is_Identity:
            unvisited.remove(g)
            break
            
    while unvisited:
        g = unvisited.pop()
        
        queue = [g]
        visited_conj = {g}
        is_ab = True
        
        # Generate the conjugacy class of g. If all elements in the conjugacy class
        # mutually commute, then the normal closure they generate is abelian.
        while queue:
            curr = queue.pop(0)
            for gen in G.generators:
                conj = gen * curr * ~gen
                if conj not in visited_conj:
                    for x in visited_conj:
                        if x * conj != conj * x:
                            is_ab = False
                            break
                    visited_conj.add(conj)
                    queue.append(conj)
                    if not is_ab:
                        break
            if not is_ab:
                break
                
        if is_ab:
            # Found a non-trivial element whose normal closure is abelian
            return False
            
        unvisited.difference_update(visited_conj)
        
    return True

def is_minimal_normal(N, G):
    """
    Checks if N is a minimal normal subgroup of G.
    """
    if N.order() == 1:
        return False
        
    # Check if N is a subgroup of G
    for n in N.generators:
        if n not in G:
            return False
            
    # Check if N is normal in G
    for n in N.generators:
        for g in G.generators:
            if g * n * ~g not in N:
                return False
                
    N_order = N.order()
    elements_N = list(N.generate())
    unvisited = set(elements_N)
    for n in elements_N:
        if n.is_Identity:
            unvisited.remove(n)
            break
            
    # Check minimality: the normal closure in G of any non-identity element in N must be N.
    while unvisited:
        n = unvisited.pop()
        
        queue = [n]
        visited_conj = {n}
        
        # Find all G-conjugates of n
        while queue:
            curr = queue.pop(0)
            for g in G.generators:
                conj = g * curr * ~g
                if conj not in visited_conj:
                    visited_conj.add(conj)
                    queue.append(conj)
                    
        # Check if these conjugates generate N
        NC_gens = [n]
        NC = PermutationGroup(NC_gens)
        reached = (NC.order() == N_order)
        
        if not reached:
            for conj in visited_conj:
                if conj not in NC:
                    NC_gens.append(conj)
                    NC = PermutationGroup(NC_gens)
                    if NC.order() == N_order:
                        reached = True
                        break
                        
        if not reached:
            return False
            
        unvisited.difference_update(visited_conj)
        
    return True

def is_non_abelian_simple(N):
    """
    A group is simple if it is a minimal normal subgroup of itself.
    """
    if N.is_abelian:
        return False
    return is_minimal_normal(N, N)

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_semisimple(G))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_minimal_normal(N, G))
    except Exception:
        h2 = False
        
    try:
        neg_q = not bool(is_non_abelian_simple(N))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: N is a minimal normal subgroup of G",
    "¬Q: N is not a non-abelian simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2