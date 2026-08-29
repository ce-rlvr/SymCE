import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            action = witness['action']
            N = witness['N']
            X_N = witness.get('X_N', None)
            X_N_provided = 'X_N' in witness
        else:
            G = witness[0]
            X = witness[1]
            action = witness[2]
            N = witness[3]
            if len(witness) > 4:
                X_N = witness[4]
                X_N_provided = True
            else:
                X_N = None
                X_N_provided = False
    except Exception:
        return [False, False, False, False, False]

    def apply_action(g, x):
        if isinstance(action, dict):
            return action[(g, x)]
        return action(g, x)

    # H1: X is a set
    try:
        h1 = isinstance(X, (set, list, tuple))
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        id_G = G.identity
        h2_id = True
        for x in X:
            if apply_action(id_G, x) != x:
                h2_id = False
                break
        
        if h2_id:
            elements = list(G.elements)
            is_left = True
            for g in elements:
                for h in elements:
                    for x in X:
                        if apply_action(g * h, x) != apply_action(g, apply_action(h, x)):
                            is_left = False
                            break
                    if not is_left: break
                if not is_left: break
                
            is_right = True
            for g in elements:
                for h in elements:
                    for x in X:
                        if apply_action(g * h, x) != apply_action(h, apply_action(g, x)):
                            is_right = False
                            break
                    if not is_right: break
                if not is_right: break
            
            h2 = is_left or is_right
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        h3 = True
        G_elements = list(G.elements)
        for gen in N.generators:
            if gen not in G_elements:
                h3 = False
                break
        if h3:
            N_elements = list(N.elements)
            for g in G.generators:
                for n in N.generators:
                    if (g * n * g**-1) not in N_elements:
                        h3 = False
                        break
                    if (g**-1 * n * g) not in N_elements:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # H4: X^N is the set of points in X fixed by every element of N
    try:
        N_elements = list(N.elements)
        expected_X_N = []
        for x in X:
            fixed = True
            for n in N_elements:
                if apply_action(n, x) != x:
                    fixed = False
                    break
            if fixed:
                expected_X_N.append(x)
                
        if X_N_provided:
            h4 = True
            for x in X_N:
                if x not in expected_X_N:
                    h4 = False
                    break
            if h4:
                for x in expected_X_N:
                    if x not in X_N:
                        h4 = False
                        break
        else:
            h4 = True
    except Exception:
        h4 = False

    # neg_Q: The set X^N is not invariant under the action of G
    try:
        actual_X_N = X_N if X_N_provided else expected_X_N
        neg_q = False
        for x in actual_X_N:
            for g in list(G.elements):
                if apply_action(g, x) not in actual_X_N:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: N is a normal subgroup of G",
    "H_4: X^N is the set of points in X fixed by every element of N",
    "¬Q: The set X^N is not invariant under the action of G"
]

N_HYP = 4
NEG_Q_INDEX = 4