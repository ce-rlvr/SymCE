import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_dict(f, Z):
    if isinstance(f, dict):
        return f
    elif isinstance(f, (list, tuple)):
        return {z: f[i] for i, z in enumerate(Z)}
    elif callable(f):
        return {z: f(z) for z in Z}
    else:
        raise ValueError("Function must be dict, list, or callable")

def conditions(witness):
    try:
        X, Y, A = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: X and Y are finite sets
    try:
        if not isinstance(X, (list, set, tuple)) or not isinstance(Y, (list, set, tuple)):
            h1 = False
        else:
            X_list = list(X)
            Y_list = list(Y)
            h1 = True
    except Exception:
        h1 = False

    # H2: A acts on both X and Y
    try:
        h2 = True
        parsed_A = []
        if not isinstance(A, (list, set, tuple)):
            h2 = False
        else:
            for a in A:
                f_X, f_Y = a
                dict_X = get_dict(f_X, X_list)
                dict_Y = get_dict(f_Y, Y_list)
                if set(dict_X.keys()) != set(X_list) or not all(v in X_list for v in dict_X.values()):
                    h2 = False
                    break
                if set(dict_Y.keys()) != set(Y_list) or not all(v in Y_list for v in dict_Y.values()):
                    h2 = False
                    break
                parsed_A.append((dict_X, dict_Y))
    except Exception:
        h2 = False

    # H3: For every a in A, the number of fixed points of a on X equals the number of fixed points of a on Y
    try:
        h3 = True
        if h2:
            for dict_X, dict_Y in parsed_A:
                fix_X = sum(1 for x in X_list if dict_X[x] == x)
                fix_Y = sum(1 for y in Y_list if dict_Y[y] == y)
                if fix_X != fix_Y:
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The number of orbits of A on X is not equal to the number of orbits of A on Y
    try:
        if not h2:
            neg_q = False
        else:
            def count_orbits(Z, acts):
                parent = {z: z for z in Z}
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
                
                for f in acts:
                    for z in Z:
                        union(z, f[z])
                
                return len(set(find(z) for z in Z))

            acts_X = [dict_X for dict_X, dict_Y in parsed_A]
            acts_Y = [dict_Y for dict_X, dict_Y in parsed_A]
            
            orbits_X = count_orbits(X_list, acts_X)
            orbits_Y = count_orbits(Y_list, acts_Y)
            
            neg_q = orbits_X != orbits_Y
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are finite sets",
    "H_2: A acts on both X and Y",
    "H_3: For every a in A, the number of fixed points of a on X equals the number of fixed points of a on Y",
    "¬Q: The number of orbits of A on X is not equal to the number of orbits of A on Y"
]

N_HYP = 3
NEG_Q_INDEX = 3