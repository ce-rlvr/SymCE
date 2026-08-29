import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import math

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

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    Witness is expected to be a tuple: (G, op, X, action, x) or (G, X, action, x)
    where G is the acting structure (e.g. a monoid), X is the set, action is the action function,
    and x is the element.
    """
    try:
        if len(witness) == 5:
            G, op, X, action, x = witness
        elif len(witness) == 4:
            G, X, action, x = witness
            op = lambda g1, g2: g1 * g2
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: X is a set
    try:
        X_list = []
        for i, y in enumerate(X):
            if i >= 1000:  # Limit size for performance
                break
            if not any(y == y_elem for y_elem in X_list):
                X_list.append(y)
        h1 = True
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        G_list = []
        for i, g in enumerate(G):
            if i >= 1000:
                break
            if not any(g == g_elem for g_elem in G_list):
                G_list.append(g)
        
        # Check closure of action
        action_valid = True
        for g in G_list:
            for y in X_list:
                val = action(g, y)
                if not any(val == y_elem for y_elem in X_list):
                    action_valid = False
                    break
            if not action_valid:
                break
        
        # Check identity existence and action
        has_identity = False
        for e in G_list:
            is_id = True
            for y in X_list:
                if action(e, y) != y:
                    is_id = False
                    break
            if is_id:
                is_G_id = True
                for g in G_list:
                    if op(e, g) != g or op(g, e) != g:
                        is_G_id = False
                        break
                if is_G_id:
                    has_identity = True
                    break
        
        # Check compatibility: g.(h.y) == (g*h).y
        compat = True
        for g in G_list:
            for h in G_list:
                for y in X_list:
                    if action(g, action(h, y)) != action(op(g, h), y):
                        compat = False
                        break
                if not compat:
                    break
            if not compat:
                break
        
        h2 = action_valid and has_identity and compat
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = any(x == y for y in X_list)
    except Exception:
        h3 = False

    # neg_Q: The cardinality of the orbit G \cdot x is NOT equal to the index of the stabilizer subgroup G_x in G
    try:
        # Compute orbit
        orbit = []
        for g in G_list:
            val = action(g, x)
            if not any(val == o for o in orbit):
                orbit.append(val)
        orbit_card = len(orbit)
        
        # Compute stabilizer
        stabilizer = []
        for g in G_list:
            if action(g, x) == x:
                stabilizer.append(g)
        
        # Compute index as the number of left cosets of the stabilizer
        cosets = []
        for g in G_list:
            coset = []
            for s in stabilizer:
                val = op(g, s)
                if not any(val == c_elem for c_elem in coset):
                    coset.append(val)
            
            is_new = True
            for c in cosets:
                if len(c) == len(coset):
                    all_in = True
                    for v in coset:
                        if not any(v == c_elem for c_elem in c):
                            all_in = False
                            break
                    if all_in:
                        is_new = False
                        break
            if is_new:
                cosets.append(coset)
        
        index_cosets = len(cosets)
        
        # The conclusion fails if the orbit cardinality does not equal the index
        neg_q = (orbit_card != index_cosets)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: The cardinality of the orbit G \\cdot x is not equal to the index of the stabilizer subgroup G_x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3