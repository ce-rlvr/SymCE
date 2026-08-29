import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    "H_1: G is a finite group",
    "H_2: |X| >= 2",
    "H_3: G acts transitively on X",
    "¬Q: Every element in G has at least one fixed point in X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    # Type 1: PermutationGroup (natural action on its degree)
    try:
        if hasattr(witness, 'is_transitive') and hasattr(witness, 'degree'):
            G = witness
            degree = G.degree
            if callable(degree):
                degree = degree()
                
            h1 = True
            h2 = bool(degree >= 2)
            
            h3_val = G.is_transitive
            if callable(h3_val):
                h3 = bool(h3_val())
            else:
                h3 = bool(h3_val)
            
            neg_q = True
            for g in G.generate():
                supp = g.support() if callable(g.support) else g.support
                # If the support size equals the degree, the permutation moves all elements (no fixed points)
                if len(supp) == degree:
                    neg_q = False
                    break
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Type 2: Tuple of (G, X, action)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, X, action = witness
            h1 = isinstance(G, (list, tuple, set))
            h2 = len(X) >= 2
            
            if h1 and h2:
                X_list = list(X)
                x0 = X_list[0]
                
                def make_hashable(item):
                    if hasattr(item, 'as_tuple'):
                        return item.as_tuple()
                    if isinstance(item, list):
                        return tuple(item)
                    if isinstance(item, set):
                        return frozenset(item)
                    return item
                
                orbit = set()
                for g in G:
                    orbit.add(make_hashable(action(g, x0)))
                    
                X_set = set(make_hashable(x) for x in X_list)
                h3 = orbit == X_set
                
                neg_q = True
                for g in G:
                    has_fixed_point = False
                    for x in X_list:
                        if action(g, x) == x:
                            has_fixed_point = True
                            break
                    if not has_fixed_point:
                        neg_q = False
                        break
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    # Type 3: Tuple of (G, X)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, X = witness
            
            # Subtype 3a: (PermutationGroup, PermutationGroup) representing (G, H) acting on cosets G/H
            if hasattr(G, 'is_group') and hasattr(X, 'is_group') and hasattr(G, 'coset_transversal'):
                H = X
                h1 = True
                cosets = G.coset_transversal(H)
                h2 = len(cosets) >= 2
                h3 = True
                
                neg_q = True
                for g in G.generate():
                    has_fixed_point = False
                    for c in cosets:
                        if H.contains(c * g * ~c) or H.contains(~c * g * c):
                            has_fixed_point = True
                            break
                    if not has_fixed_point:
                        neg_q = False
                        break
                return [h1, h2, h3, neg_q]
            
            # Subtype 3b: G is a collection of operators, X is a collection of elements
            h1 = isinstance(G, (list, tuple, set))
            h2 = len(X) >= 2
            
            if h1 and h2:
                X_list = list(X)
                x0 = X_list[0]
                
                def apply_action(g, x):
                    if callable(g):
                        return g(x)
                    return g * x
                
                def make_hashable(item):
                    if hasattr(item, 'as_tuple'):
                        return item.as_tuple()
                    if isinstance(item, list):
                        return tuple(item)
                    if isinstance(item, set):
                        return frozenset(item)
                    return item
                
                orbit = set()
                for g in G:
                    orbit.add(make_hashable(apply_action(g, x0)))
                    
                X_set = set(make_hashable(x) for x in X_list)
                h3 = orbit == X_set
                
                neg_q = True
                for g in G:
                    has_fixed_point = False
                    for x in X_list:
                        if apply_action(g, x) == x:
                            has_fixed_point = True
                            break
                    if not has_fixed_point:
                        neg_q = False
                        break
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False, False]