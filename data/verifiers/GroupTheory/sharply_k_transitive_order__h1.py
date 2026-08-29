import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: X is a finite set of size n",
    "H_2: k is a positive integer such that k <= n",
    "H_3: G acts sharply k-transitively on X",
    "¬Q: The order of the group G is not exactly n(n-1)...(n-k+1)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) == 3:
            G, X, k = witness
        else:
            return [False, False, False, False]
            
        # Allow X to be specified as an integer n for convenience
        if isinstance(X, int):
            X = list(range(X))
    except Exception:
        return [False, False, False, False]

    # H_1: Let X be a finite set of size n.
    try:
        if not isinstance(X, (set, list, tuple)):
            h1 = False
        else:
            X_list = list(X)
            if len(set(X_list)) != len(X_list):
                h1 = False
            else:
                n = len(X_list)
                h1 = True
    except Exception:
        h1 = False

    # H_2: Let k be a positive integer such that k <= n.
    try:
        if h1 and isinstance(k, int) and k > 0 and k <= n:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: Let G act sharply k-transitively on X.
    try:
        if not (h1 and h2):
            h3 = False
        elif not isinstance(G, PermutationGroup):
            h3 = False
        else:
            X_list = list(X)
            X_set = set(X_list)
            is_invariant = True
            
            # Check if X is invariant under the action of G
            for g in G.generators:
                for x in X_set:
                    if g(x) not in X_set:
                        is_invariant = False
                        break
                if not is_invariant:
                    break
            
            if not is_invariant:
                h3 = False
            else:
                # Construct the induced permutation group G_X on X
                x_to_i = {x: i for i, x in enumerate(X_list)}
                gens_X = []
                for g in G.generators:
                    images = [x_to_i[g(x)] for x in X_list]
                    gens_X.append(Permutation(images))
                
                if not gens_X:
                    gens_X = [Permutation(n - 1)]
                    
                G_X = PermutationGroup(gens_X)
                target_order = math.perm(n, k)
                
                # For sharply k-transitive action, the induced group must have the exact target order
                if G_X.order() != target_order:
                    h3 = False
                else:
                    # Check if the induced action is k-transitive by computing the orbit of one k-tuple
                    start_tuple = tuple(range(k))
                    visited = set([start_tuple])
                    queue = [start_tuple]
                    idx = 0
                    while idx < len(queue):
                        curr = queue[idx]
                        idx += 1
                        for g in gens_X:
                            next_tuple = tuple(g(c) for c in curr)
                            if next_tuple not in visited:
                                visited.add(next_tuple)
                                queue.append(next_tuple)
                    
                    h3 = (len(visited) == target_order)
    except Exception:
        h3 = False

    # ¬Q: The order of the group G is exactly n(n-1)...(n-k+1).
    # Negation: The order of G is NOT exactly n(n-1)...(n-k+1).
    try:
        if h1 and h2:
            target_order = math.perm(n, k)
            neg_q = (G.order() != target_order)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]