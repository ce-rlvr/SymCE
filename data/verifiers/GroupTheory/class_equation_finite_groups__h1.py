import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Class Equation conjecture.
    The witness is expected to be a tuple: (G, Z, X, C)
    where:
      - G is the group
      - Z is the center of G
      - X is a list of representatives of conjugacy classes of size > 1
      - C is a list of centralizers corresponding to X
    """
    try:
        G, Z, X, C = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: Z(G) is the center of G
    try:
        if hasattr(G, 'center') and callable(G.center):
            h1 = (Z == G.center())
        elif hasattr(G, 'center'):
            h1 = (Z == G.center)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: {x_1, ..., x_k} is a complete set of representatives of the distinct conjugacy classes of G of size > 1
    try:
        if hasattr(G, 'conjugacy_classes') and callable(G.conjugacy_classes):
            classes = G.conjugacy_classes()
            classes_gt_1 = []
            for c in classes:
                if hasattr(c, 'size'):
                    if c.size > 1:
                        classes_gt_1.append(c)
                else:
                    if len(list(c)) > 1:
                        classes_gt_1.append(c)
            
            if len(X) == len(classes_gt_1):
                h2 = True
                for c in classes_gt_1:
                    overlap = [x for x in X if x in c]
                    if len(overlap) != 1:
                        h2 = False
                        break
            else:
                h2 = False
        elif hasattr(G, 'reps'):
            h2 = (X == G.reps)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: C_G(x_i) is the centralizer of x_i in G
    try:
        if hasattr(G, 'centralizer') and callable(G.centralizer):
            if len(X) != len(C):
                h3 = False
            else:
                h3 = True
                for x, c in zip(X, C):
                    if c != G.centralizer(x):
                        h3 = False
                        break
        elif hasattr(G, 'centralizers'):
            h3 = (C == G.centralizers)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: |G| != |Z(G)| + sum_{i=1}^k (G : C_G(x_i))
    try:
        if hasattr(G, 'order') and callable(G.order):
            g_ord = G.order()
        else:
            g_ord = G.order
            
        if hasattr(Z, 'order') and callable(Z.order):
            z_ord = Z.order()
        else:
            z_ord = Z.order
            
        indices = []
        for c in C:
            if hasattr(c, 'index_in'):
                idx = c.index_in(G) if callable(c.index_in) else c.index_in
            elif hasattr(c, 'index'):
                idx = c.index() if callable(c.index) else c.index
            else:
                if hasattr(c, 'order') and callable(c.order):
                    c_ord = c.order()
                else:
                    c_ord = c.order
                idx = g_ord / c_ord
            indices.append(idx)
            
        rhs = z_ord + sum(indices)
        neg_q = (g_ord != rhs)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: {x_1, ..., x_k} is a complete set of representatives of the distinct conjugacy classes of G of size greater than 1",
    "H_3: C_G(x_i) is the centralizer of x_i in G",
    "not Q: |G| != |Z(G)| + sum_{i=1}^k (G : C_G(x_i))"
]

N_HYP = 3
NEG_Q_INDEX = 3