import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def apply_perm(g, x):
    """Safely apply a permutation, function, or dictionary to an element x."""
    try:
        if hasattr(g, 'size') and hasattr(x, '__int__'):
            x_int = int(x)
            if 0 <= x_int < g.size:
                return g(x_int)
            else:
                return x_int
        elif isinstance(g, dict):
            return g.get(x, x)
        else:
            return g(x)
    except Exception:
        return x

def conditions(witness) -> list[bool]:
    # Parse the witness into a set X and a collection of transformations G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            X_obj, G_obj = witness
            try:
                X = list(X_obj)
            except TypeError:
                X = [X_obj]
            try:
                G = list(G_obj)
            except TypeError:
                G = [G_obj]
        else:
            try:
                G = list(witness)
            except TypeError:
                G = [witness]
            
            max_point = -1
            for p in G:
                if hasattr(p, 'size'):
                    max_point = max(max_point, p.size - 1)
            if max_point >= 0:
                X = list(range(max_point + 1))
            else:
                X = []
    except Exception:
        X = []
        G = []

    # H_1: X is a finite set
    try:
        h1 = isinstance(X, list)
    except Exception:
        h1 = False

    # H_2: |X| >= 2
    try:
        h2 = len(set(X)) >= 2
    except Exception:
        h2 = False

    # H_3: The action of G on X is transitive
    try:
        h3 = False
        if X:
            X_unique = set(X)
            visited = set()
            start = next(iter(X_unique))
            queue = [start]
            visited.add(start)
            
            # BFS to find the orbit of 'start' under G
            while queue:
                curr = queue.pop(0)
                for g in G:
                    nxt = apply_perm(g, curr)
                    if nxt in X_unique and nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
            
            h3 = (visited == X_unique)
    except Exception:
        h3 = False

    # ¬Q: Every element g in G has at least one fixed point in X
    try:
        neg_q = True
        for g in G:
            has_fixed = False
            for x in X:
                if apply_perm(g, x) == x:
                    has_fixed = True
                    break
            if not has_fixed:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a finite set",
    "H_2: |X| >= 2",
    "H_3: The action of G on X is transitive",
    "¬Q: Every element g in G has at least one fixed point in X"
]

N_HYP = 3
NEG_Q_INDEX = 3