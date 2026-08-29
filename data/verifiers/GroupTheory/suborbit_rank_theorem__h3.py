import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: The action of G on X is transitive",
    "H_3: x is a fixed element of X, and G_x is its stabilizer in G",
    r"¬Q: The number of orbits of G on X \times X is not equal to the number of orbits of G_x on X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def apply_action(g, y):
    try:
        return g(y)
    except Exception:
        return g * y

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, X = witness
            try:
                X_list = sorted(list(X)) if isinstance(X, (set, frozenset)) else list(X)
            except TypeError:
                X_list = list(X)
            x = X_list[0] if X_list else None
            return G, X_list, x
        elif len(witness) >= 3:
            G, X, x = witness[:3]
            try:
                X_list = sorted(list(X)) if isinstance(X, (set, frozenset)) else list(X)
            except TypeError:
                X_list = list(X)
            return G, X_list, x
    else:
        G = witness
        if hasattr(G, 'degree'):
            X_list = list(range(G.degree))
        else:
            X_list = []
        x = X_list[0] if X_list else None
        return G, X_list, x
    return None, None, None

def conditions(witness) -> list[bool]:
    G, X, x = parse_witness(witness)
    
    # H1: G is a group acting on a set X
    h1 = False
    try:
        if hasattr(G, 'generators') and isinstance(X, list):
            X_set = set(X)
            acts = True
            for g in G.generators:
                for y in X:
                    if apply_action(g, y) not in X_set:
                        acts = False
                        break
                if not acts:
                    break
            h1 = acts
    except Exception:
        h1 = False

    # H2: The action of G on X is transitive
    h2 = False
    try:
        if h1 and X:
            X_set = set(X)
            orbit = set([X[0]])
            queue = [X[0]]
            while queue:
                curr = queue.pop(0)
                for g in G.generators:
                    nxt = apply_action(g, curr)
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            h2 = (orbit == X_set)
    except Exception:
        h2 = False

    # H3: x is a fixed element of X, and G_x is its stabilizer in G
    h3 = False
    try:
        if h1 and X:
            h3 = (x in X)
            if h3:
                if not hasattr(G, 'stabilizer'):
                    h3 = False
                else:
                    G_x = G.stabilizer(x)
                    if not hasattr(G_x, 'generators'):
                        h3 = False
    except Exception:
        h3 = False

    # neg_Q: The number of orbits of G on X \times X is NOT equal to the number of orbits of G_x on X
    neg_q = False
    try:
        if h1 and h3:
            # Orbits of G on X x X
            pairs = [(a, b) for a in X for b in X]
            visited_pairs = set()
            orbits_XX = 0
            for start in pairs:
                if start not in visited_pairs:
                    orbits_XX += 1
                    queue = [start]
                    visited_pairs.add(start)
                    while queue:
                        curr = queue.pop(0)
                        for g in G.generators:
                            nxt = (apply_action(g, curr[0]), apply_action(g, curr[1]))
                            if nxt not in visited_pairs:
                                visited_pairs.add(nxt)
                                queue.append(nxt)
            
            # Orbits of G_x on X
            G_x = G.stabilizer(x)
            visited_X = set()
            orbits_Gx_X = 0
            for start in X:
                if start not in visited_X:
                    orbits_Gx_X += 1
                    queue = [start]
                    visited_X.add(start)
                    while queue:
                        curr = queue.pop(0)
                        for h in G_x.generators:
                            nxt = apply_action(h, curr)
                            if nxt not in visited_X:
                                visited_X.add(nxt)
                                queue.append(nxt)
            
            neg_q = (orbits_XX != orbits_Gx_X)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]