import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def apply_action(f, a):
    if isinstance(f, dict):
        return f[a]
    elif hasattr(f, '__call__'):
        return f(a)
    elif hasattr(f, '__getitem__'):
        return f[a]
    else:
        return f(a)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    # Extract witness components
    if isinstance(witness, dict):
        X = witness.get('X')
        G = witness.get('G')
        x = witness.get('x')
        y = witness.get('y')
        G_x_wit = witness.get('G_x')
        G_y_wit = witness.get('G_y')
    else:
        X = getattr(witness, 'X', None)
        G = getattr(witness, 'G', None)
        x = getattr(witness, 'x', None)
        y = getattr(witness, 'y', None)
        G_x_wit = getattr(witness, 'G_x', None)
        G_y_wit = getattr(witness, 'G_y', None)

    # H1: X is a finite set on which G acts transitively
    h1 = False
    try:
        if X is not None and G is not None:
            X_list = list(X)
            G_elements = get_elements(G)
            if len(X_list) > 0 and len(G_elements) > 0:
                is_transitive = True
                for a in X_list:
                    for b in X_list:
                        if not any(apply_action(f, a) == b for f in G_elements):
                            is_transitive = False
                            break
                    if not is_transitive:
                        break
                h1 = is_transitive
    except Exception:
        h1 = False

    # H2: x and y are elements of X
    h2 = False
    try:
        if X is not None and x is not None and y is not None:
            X_list = list(X)
            h2 = (x in X_list) and (y in X_list)
    except Exception:
        h2 = False

    # H3: G_x and G_y are the stabilizers of x and y in G, respectively
    h3 = False
    try:
        if h1 and h2:
            X_list = list(X)
            G_elements = get_elements(G)
            G_x_true = [f for f in G_elements if apply_action(f, x) == x]
            G_y_true = [f for f in G_elements if apply_action(f, y) == y]
            
            if G_x_wit is not None and G_y_wit is not None:
                G_x_wit_elems = get_elements(G_x_wit)
                G_y_wit_elems = get_elements(G_y_wit)
                
                def is_same_subset(sub1, sub2):
                    for f in sub1:
                        if not any(all(apply_action(f, a) == apply_action(g, a) for a in X_list) for g in sub2):
                            return False
                    for g in sub2:
                        if not any(all(apply_action(f, a) == apply_action(g, a) for a in X_list) for f in sub1):
                            return False
                    return True
                
                h3 = is_same_subset(G_x_wit_elems, G_x_true) and is_same_subset(G_y_wit_elems, G_y_true)
            else:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: The cardinality of the orbit of y under G_x is NOT equal to the cardinality of the orbit of x under G_y
    neg_q = False
    try:
        if h1 and h2 and h3:
            G_elements = get_elements(G)
            if G_x_wit is not None:
                G_x_use = get_elements(G_x_wit)
            else:
                G_x_use = [f for f in G_elements if apply_action(f, x) == x]
                
            if G_y_wit is not None:
                G_y_use = get_elements(G_y_wit)
            else:
                G_y_use = [f for f in G_elements if apply_action(f, y) == y]
            
            orbit_y = set(apply_action(f, y) for f in G_x_use)
            orbit_x = set(apply_action(f, x) for f in G_y_use)
            
            neg_q = len(orbit_y) != len(orbit_x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a finite set on which G acts transitively",
    "H_2: x and y are elements of X",
    "H_3: G_x and G_y are the stabilizers of x and y in G, respectively",
    "¬Q: The cardinality of the orbit of y under G_x is NOT equal to the cardinality of the orbit of x under G_y"
]

N_HYP = 3
NEG_Q_INDEX = 3