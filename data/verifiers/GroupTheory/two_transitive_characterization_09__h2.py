import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_transitive(G, X, action):
    """Check if G acts transitively on X."""
    if not X:
        return True
    orb = set()
    queue = [X[0]]
    orb.add(X[0])
    
    gens = G.generators if hasattr(G, 'generators') else G
        
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = action(g, curr)
            if nxt not in orb:
                orb.add(nxt)
                queue.append(nxt)
    return len(orb) == len(X)

def is_2_transitive(G, X, action):
    """Check if G acts 2-transitively on X."""
    if len(X) < 2:
        return False
    pairs = [(a, b) for a in X for b in X if a != b]
    if not pairs:
        return True
    
    orb = set()
    p0 = pairs[0]
    queue = [p0]
    orb.add(p0)
    
    gens = G.generators if hasattr(G, 'generators') else G
        
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = (action(g, curr[0]), action(g, curr[1]))
            if nxt not in orb:
                orb.add(nxt)
                queue.append(nxt)
    return len(orb) == len(pairs)

def check_rhs(G, X, action, is_default):
    """Check if G acts transitively on X and for any x in X, G_x acts transitively on X \ {x}."""
    if not is_transitive(G, X, action):
        return False
    
    for x in X:
        if is_default and hasattr(G, 'stabilizer'):
            Gx = G.stabilizer(x)
            if not is_transitive(Gx, [y for y in X if y != x], action):
                return False
        else:
            elements = list(G.elements) if hasattr(G, 'elements') else list(G)
            Gx_elements = [g for g in elements if action(g, x) == x]
            if not is_transitive(Gx_elements, [y for y in X if y != x], action):
                return False
    return True

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, X = witness
                action = lambda g, x: g(x)
                is_default = True
            elif len(witness) == 3:
                G, X, action = witness
                is_default = False
            else:
                return [False, False, False]
        else:
            G = witness
            if not hasattr(G, 'degree'):
                return [False, False, False]
            X = list(range(G.degree))
            action = lambda g, x: g(x)
            is_default = True
            
        # H_1: G is a group
        h1 = hasattr(G, 'elements') or hasattr(G, 'generators') or isinstance(G, list)
        if not h1:
            return [False, False, False]
            
        # H_2: G acts on X
        h2 = True
        gens = G.generators if hasattr(G, 'generators') else G
        for g in gens:
            for x in X:
                res = action(g, x)
                if res not in X:
                    h2 = False
                    break
            if not h2:
                break
                
        if not h2:
            return [True, False, False]
            
        # ¬Q: The equivalence fails
        lhs = is_2_transitive(G, X, action)
        rhs = check_rhs(G, X, action, is_default)
        neg_q = (lhs != rhs)
        
        return [True, True, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "¬Q: G acts 2-transitively on X is NOT equivalent to (G acts transitively on X and for any x in X, G_x acts transitively on X \\ {x})"
]

N_HYP = 2
NEG_Q_INDEX = 2