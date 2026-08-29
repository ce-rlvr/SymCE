import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, X, N = witness
        elif len(witness) == 2:
            G, N = witness
            X = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: X is a set
    try:
        if X is None:
            h2 = True
            degree = max(G.degree if h1 else 0, N.degree if isinstance(N, PermutationGroup) else 0)
        elif isinstance(X, (set, list, tuple)):
            h2 = True
            degree = len(X)
        elif isinstance(X, int) and X >= 0:
            h2 = True
            degree = X
        else:
            h2 = False
            degree = max(G.degree if h1 else 0, N.degree if isinstance(N, PermutationGroup) else 0)
            
        if h1:
            degree = max(degree, G.degree)
        if isinstance(N, PermutationGroup):
            degree = max(degree, N.degree)
    except Exception:
        h2 = False
        degree = 0
        
    # H3: N is a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup) or not h1:
            h3 = False
        else:
            is_sub = True
            for g in N.generators:
                if not G.contains(g):
                    is_sub = False
                    break
            
            is_normal = is_sub
            if is_sub:
                for g in G.generators:
                    for n in N.generators:
                        conj1 = (~g) * n * g
                        conj2 = g * n * (~g)
                        if not (N.contains(conj1) and N.contains(conj2)):
                            is_normal = False
                            break
                    if not is_normal:
                        break
            h3 = is_normal
    except Exception:
        h3 = False
        
    # neg_Q: The set of orbits of N on X does NOT form a system of imprimitivity for G on X.
    # A system of imprimitivity requires the group action to be transitive.
    try:
        if not h1 or not isinstance(N, PermutationGroup):
            neg_q = False
        elif degree == 0:
            is_system_of_imprimitivity = True
            neg_q = not is_system_of_imprimitivity
        else:
            # Check transitivity of G on the domain
            visited = set([0])
            queue = [0]
            while queue:
                x = queue.pop(0)
                for g in G.generators:
                    gx = g(x) if x < g.size else x
                    if gx not in visited:
                        visited.add(gx)
                        queue.append(gx)
            is_transitive = (len(visited) == degree)
            
            # Find orbits of N on the domain
            parent = {i: i for i in range(degree)}
            def find(i):
                if parent[i] == i:
                    return i
                parent[i] = find(parent[i])
                return parent[i]
            def union(i, j):
                root_i = find(i)
                root_j = find(j)
                if root_i != root_j:
                    parent[root_i] = root_j

            for n in N.generators:
                for i in range(degree):
                    ni = n(i) if i < n.size else i
                    union(i, ni)
                    
            orbits = {}
            for i in range(degree):
                root = find(i)
                orbits.setdefault(root, set()).add(i)
                
            partition = set(frozenset(o) for o in orbits.values())
            
            # Check if G permutes the blocks (orbits of N)
            permutes_blocks = True
            for g in G.generators:
                for block in partition:
                    mapped_block = frozenset((g(x) if x < g.size else x) for x in block)
                    if mapped_block not in partition:
                        permutes_blocks = False
                        break
                if not permutes_blocks:
                    break
                    
            is_system_of_imprimitivity = is_transitive and permutes_blocks
            neg_q = not is_system_of_imprimitivity
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: N is a normal subgroup of G",
    "¬Q: The orbits of N do not form a system of imprimitivity for G on X"
]

N_HYP = 3
NEG_Q_INDEX = 3