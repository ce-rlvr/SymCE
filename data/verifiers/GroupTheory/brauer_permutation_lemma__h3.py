import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    witness is expected to be a tuple: (A, X, Y, action_X, action_Y)
    where:
      - A is a finite group (e.g., a sympy PermutationGroup)
      - X and Y are iterables representing finite sets
      - action_X is a callable f(a, x) returning an element of X
      - action_Y is a callable f(a, y) returning an element of Y
    """
    try:
        A, X, Y, action_X, action_Y = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: A is a finite group
    try:
        if isinstance(A, PermutationGroup):
            h1 = True
            A_elements = list(A.elements)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: X and Y are finite sets
    try:
        X_list = list(X)
        Y_list = list(Y)
        h2 = True
    except Exception:
        h2 = False

    # H3: For every a in A, the number of fixed points of a on X equals the number of fixed points of a on Y
    try:
        h3 = True
        if h1 and h2:
            for a in A_elements:
                fix_X = 0
                for x in X_list:
                    res = action_X(a, x)
                    if res not in X_list:
                        h3 = False
                        break
                    if res == x:
                        fix_X += 1
                if not h3: break
                
                fix_Y = 0
                for y in Y_list:
                    res = action_Y(a, y)
                    if res not in Y_list:
                        h3 = False
                        break
                    if res == y:
                        fix_Y += 1
                if not h3: break
                
                if fix_X != fix_Y:
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The number of orbits of A on X is NOT equal to the number of orbits of A on Y
    try:
        def get_orbits(Z_list, action):
            n = len(Z_list)
            parent = list(range(n))
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
                    
            for i in range(n):
                z = Z_list[i]
                for a in A_elements:
                    res = action(a, z)
                    try:
                        j = Z_list.index(res)
                        union(i, j)
                    except ValueError:
                        pass
                        
            orbits = set()
            for i in range(n):
                orbits.add(find(i))
            return len(orbits)
            
        if h1 and h2:
            orbits_X = get_orbits(X_list, action_X)
            orbits_Y = get_orbits(Y_list, action_Y)
            neg_q = (orbits_X != orbits_Y)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a finite group",
    "H_2: X and Y are finite sets",
    "H_3: For every a in A, the number of fixed points of a on X equals the number of fixed points of a on Y",
    "¬Q: The number of orbits of A on X is not equal to the number of orbits of A on Y"
]

N_HYP = 3
NEG_Q_INDEX = 3