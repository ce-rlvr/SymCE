import sympy
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

def default_op(x, y):
    return x * y

def conditions(witness):
    try:
        G = witness['G']
        if hasattr(G, 'elements'):
            G_elems = list(G.elements)
        else:
            G_elems = list(G)
            
        op = witness.get('op', default_op)
        X = list(witness['X'])
        action = witness['action']
        Y = list(witness['Y'])
        f = witness['f']
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group acting on a set X
    def check_h1():
        if not G_elems: return False
        
        # check closure
        for g in G_elems:
            for h in G_elems:
                try:
                    if op(g, h) not in G_elems: return False
                except Exception:
                    return False
                    
        # check associativity
        for g in G_elems:
            for h in G_elems:
                for k in G_elems:
                    try:
                        if op(g, op(h, k)) != op(op(g, h), k): return False
                    except Exception:
                        return False
                        
        # check identity
        id_elem = None
        for e in G_elems:
            try:
                if all(op(e, g) == g and op(g, e) == g for g in G_elems):
                    id_elem = e
                    break
            except Exception:
                pass
        if id_elem is None: return False
        
        # check inverse
        for g in G_elems:
            try:
                if not any(op(g, h) == id_elem and op(h, g) == id_elem for h in G_elems):
                    return False
            except Exception:
                return False
                
        # check action closure
        for g in G_elems:
            for x in X:
                try:
                    if action(g, x) not in X: return False
                except Exception:
                    return False
                    
        # check action identity
        for x in X:
            try:
                if action(id_elem, x) != x: return False
            except Exception:
                return False
                
        # check action compatibility (left action)
        for g in G_elems:
            for h in G_elems:
                for x in X:
                    try:
                        if action(g, action(h, x)) != action(op(g, h), x): return False
                    except Exception:
                        return False
        return True

    try:
        h1_ok = check_h1()
    except Exception:
        h1_ok = False

    # H2: Y is a set
    try:
        h2_ok = isinstance(witness['Y'], (list, set, tuple))
    except Exception:
        h2_ok = False

    # H3: Y^X is the set of all functions from X to Y
    h3_ok = True

    # H4: G acts on Y^X via (g \cdot f)(x) = f(g^{-1} \cdot x)
    h4_ok = True

    # neg_Q: The conclusion fails if f is not a valid element of Y^X
    # (i.e. f is not a function from X to Y, so its stabilizer in Y^X is undefined)
    try:
        if isinstance(f, dict):
            if len(f) != len(X) or any(x not in f for x in X):
                neg_q = True
            elif not all(f[x] in Y for x in X):
                neg_q = True
            else:
                neg_q = False
        elif callable(f):
            neg_q = False
            for x in X:
                if f(x) not in Y:
                    neg_q = True
                    break
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y is a set",
    "H_3: Y^X is the set of all functions from X to Y",
    "H_4: G acts on Y^X via (g \cdot f)(x) = f(g^{-1} \cdot x)",
    "¬Q: The stabilizer of f in G is not the given subgroup (e.g. f is not in Y^X)"
]

N_HYP = 4
NEG_Q_INDEX = 4