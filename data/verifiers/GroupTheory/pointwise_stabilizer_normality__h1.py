import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: Y is a subset of X",
    "¬Q: The pointwise stabilizer G_{(Y)} is not a normal subgroup of the setwise stabilizer G_{Y}"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            G, Y = witness
            X_given = None
            action = None
        elif len(witness) == 3:
            if callable(witness[2]):
                G, Y, action = witness
                X_given = None
            else:
                G, X_given, Y = witness
                action = None
        elif len(witness) == 4:
            G, X_given, Y, action = witness
        else:
            return [False, False]
            
        Y_set = set(Y)
        
        # Fast path for standard PermutationGroup with default action
        if isinstance(G, PermutationGroup) and action is None:
            if X_given is None:
                X = set(range(G.degree))
            else:
                X = set(X_given)
            h1 = Y_set.issubset(X)
            # For a true group acting via permutations, the pointwise stabilizer 
            # is ALWAYS a normal subgroup of the setwise stabilizer.
            return [h1, False]
            
        # General case evaluation
        if isinstance(G, PermutationGroup):
            if G.order() > 10000:
                return [False, False]
            elements = list(G.elements)
            if X_given is None:
                X = set(range(G.degree))
            else:
                X = set(X_given)
        elif isinstance(G, (list, set, tuple)):
            elements = list(G)
            if not elements:
                return [False, False]
            first = elements[0]
            if X_given is None:
                if isinstance(first, Permutation):
                    n = max(g.size for g in elements) if any(g.size > 0 for g in elements) else 0
                    X = set(range(n))
                elif isinstance(first, tuple):
                    n = len(first)
                    X = set(range(n))
                elif hasattr(first, 'is_Identity'):
                    return [False, False] # X must be provided for matrices
                else:
                    return [False, False]
            else:
                X = set(X_given)
        else:
            return [False, False]
            
        h1 = Y_set.issubset(X)
        
        first = elements[0]
        if isinstance(first, Permutation):
            def multiply(a, b): return a * b
            def is_identity(a): return a.is_Identity
            if action is None:
                def apply(g, x): return g(x)
            else:
                def apply(g, x): return action(g, x)
        elif isinstance(first, tuple):
            def multiply(a, b): return tuple(a[b[i]] for i in range(len(a)))
            def is_identity(a): return a == tuple(range(len(a)))
            if action is None:
                def apply(g, x): return g[x]
            else:
                def apply(g, x): return action(g, x)
        elif hasattr(first, 'is_Identity') and hasattr(first, '__mul__'):
            def multiply(a, b): return a * b
            def is_identity(a): return a.is_Identity
            if action is None:
                def apply(g, x): return g * x
            else:
                def apply(g, x): return action(g, x)
        else:
            return [False, False]
            
        G_Y = []
        G_p = []
        for g in elements:
            try:
                image = {apply(g, y) for y in Y_set}
                if image == Y_set:
                    G_Y.append(g)
                if all(apply(g, y) == y for y in Y_set):
                    G_p.append(g)
            except Exception:
                pass
                
        def is_group(subset):
            if not subset:
                return False
            has_id = any(is_identity(s) for s in subset)
            if not has_id:
                return False
            
            try:
                subset_set = set(subset)
                def in_subset(x): return x in subset_set
            except TypeError:
                def in_subset(x): return x in subset
                
            for a in subset:
                for b in subset:
                    if not in_subset(multiply(a, b)):
                        return False
            for a in subset:
                has_inv = False
                for b in subset:
                    if is_identity(multiply(a, b)) and is_identity(multiply(b, a)):
                        has_inv = True
                        break
                if not has_inv:
                    return False
            return True

        if not is_group(G_Y):
            neg_q = True
        elif not is_group(G_p):
            neg_q = True
        else:
            inverses = {}
            for g in G_Y:
                for b in G_Y:
                    if is_identity(multiply(g, b)) and is_identity(multiply(b, g)):
                        inverses[g] = b
                        break
            
            try:
                G_p_set = set(G_p)
                def in_G_p(x): return x in G_p_set
            except TypeError:
                def in_G_p(x): return x in G_p
                
            is_normal = True
            for g in G_Y:
                g_inv = inverses.get(g)
                if g_inv is None:
                    is_normal = False
                    break
                for h in G_p:
                    conj = multiply(multiply(g, h), g_inv)
                    if not in_G_p(conj):
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
            
        return [h1, neg_q]
    except Exception:
        return [False, False]