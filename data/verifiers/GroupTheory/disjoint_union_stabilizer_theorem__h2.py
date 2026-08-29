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

def has_duplicates(lst):
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]: 
                return True
    return False

def conditions(witness):
    try:
        G = witness['G']
        op = witness['op']
        X = witness['X']
        Y = witness['Y']
        XY = witness['XY']
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        action_XY = witness['action_XY']
        x = witness['x']
    except Exception:
        return [False] * 4 + [False]

    def check_group():
        try:
            if not G: return False
            if has_duplicates(G): return False
            for g in G:
                for h in G:
                    if op(g, h) not in G: return False
            for g in G:
                for h in G:
                    for k in G:
                        if op(op(g, h), k) != op(g, op(h, k)): return False
            id_elements = []
            for e in G:
                if all(op(e, g) == g and op(g, e) == g for g in G):
                    id_elements.append(e)
            if len(id_elements) != 1: return False
            e = id_elements[0]
            for g in G:
                if not any(op(g, h) == e and op(h, g) == e for h in G): return False
            return True
        except Exception:
            return False

    h1 = check_group()

    def check_action(Z, action):
        try:
            if not isinstance(Z, (list, tuple)): return False
            if has_duplicates(Z): return False
            for g in G:
                for z in Z:
                    if action(g, z) not in Z: return False
            e = [e for e in G if all(op(e, g) == g for g in G)][0]
            for z in Z:
                if action(e, z) != z: return False
            for g in G:
                for h in G:
                    for z in Z:
                        if action(op(g, h), z) != action(g, action(h, z)): return False
            return True
        except Exception:
            return False

    h2 = False
    if h1:
        h2 = check_action(X, action_X) and check_action(Y, action_Y)

    def check_h3():
        try:
            if not check_action(XY, action_XY): return False
            if len(XY) != len(X) + len(Y): return False
            for g in G:
                for z in XY:
                    if z in X:
                        if action_XY(g, z) != action_X(g, z): return False
                    if z in Y:
                        if action_XY(g, z) != action_Y(g, z): return False
            return True
        except Exception:
            return False

    h3 = False
    if h1:
        h3 = check_h3()

    def check_h4():
        try:
            return x in X
        except Exception:
            return False

    h4 = check_h4()

    def check_neg_q():
        try:
            stab_X = []
            for g in G:
                try:
                    if action_X(g, x) == x:
                        if g not in stab_X: stab_X.append(g)
                except Exception:
                    pass
            stab_XY = []
            for g in G:
                try:
                    if action_XY(g, x) == x:
                        if g not in stab_XY: stab_XY.append(g)
                except Exception:
                    pass
            
            for g in stab_X:
                if g not in stab_XY: return True
            for g in stab_XY:
                if g not in stab_X: return True
            return False
        except Exception:
            return False

    neg_q = False
    if h1 and h4:
        neg_q = check_neg_q()

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X and G acts on Y",
    "H_3: G acts on the disjoint union X \sqcup Y such that g \cdot z is defined by the action on X if z \in X, and by the action on Y if z \in Y",
    "H_4: x is an element of X",
    "¬Q: The stabilizer of x under the action of G on X \sqcup Y is NOT equal to the stabilizer of x under the action of G on X"
]

N_HYP = 4
NEG_Q_INDEX = 4