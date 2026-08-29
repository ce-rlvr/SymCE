import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer, Symbol
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: Let ~_p be the relation on X defined by continuous paths",
    "¬Q: The relation ~_p is not an equivalence relation or its classes do not partition X"
]

def extract_X_R(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        X, R = witness
        try:
            X_list = list(X)
            return X_list, R
        except TypeError:
            pass
            
    if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
        rows, cols = witness.shape
        if rows == cols:
            X = list(range(rows))
            R = []
            for i in range(rows):
                for j in range(cols):
                    if witness[i, j]:
                        R.append((i, j))
            return X, R

    if isinstance(witness, dict):
        X = list(witness.keys())
        R = []
        for u, neighbors in witness.items():
            for v in neighbors:
                R.append((u, v))
        return X, R

    if hasattr(witness, '__iter__') and not isinstance(witness, (str, dict)):
        R = list(witness)
        X_list = []
        for item in R:
            if isinstance(item, tuple) and len(item) == 2:
                if item[0] not in X_list:
                    X_list.append(item[0])
                if item[1] not in X_list:
                    X_list.append(item[1])
            else:
                return None, None
        return X_list, R

    return None, None

def conditions(witness):
    try:
        X, R = extract_X_R(witness)
        if X is None:
            return [False, False]
            
        unique_X = []
        for x in X:
            if x not in unique_X:
                unique_X.append(x)
        X = unique_X

        if callable(R):
            rel = R
            h1 = True
        else:
            R_list = list(R)
            try:
                R_set = set(R_list)
                def rel(x, y):
                    return (x, y) in R_set
                X_set = set(X)
                h1 = True
                for item in R_set:
                    if not isinstance(item, tuple) or len(item) != 2:
                        h1 = False
                        break
                    if item[0] not in X_set or item[1] not in X_set:
                        h1 = False
                        break
            except TypeError:
                def rel(x, y):
                    return (x, y) in R_list
                h1 = True
                for item in R_list:
                    if not isinstance(item, tuple) or len(item) != 2:
                        h1 = False
                        break
                    if item[0] not in X or item[1] not in X:
                        h1 = False
                        break
    except Exception:
        return [False, False]

    try:
        reflexive = all(rel(x, x) for x in X)
        symmetric = all(rel(x, y) == rel(y, x) for x in X for y in X)
        transitive = all(not (rel(x, y) and rel(y, z)) or rel(x, z) for x in X for y in X for z in X)
        
        is_equiv = reflexive and symmetric and transitive
        
        if is_equiv:
            classes = []
            for x in X:
                found = False
                for c in classes:
                    if x in c:
                        found = True
                        break
                if not found:
                    cls = [y for y in X if rel(x, y)]
                    classes.append(cls)
            
            disjoint = True
            for i in range(len(classes)):
                for j in range(i+1, len(classes)):
                    if any(item in classes[j] for item in classes[i]):
                        disjoint = False
            
            covered_len = sum(len(c) for c in classes)
            partitions = disjoint and covered_len == len(X)
        else:
            partitions = False
            
        q = is_equiv and partitions
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]