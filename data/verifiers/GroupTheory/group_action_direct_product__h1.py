import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    # H_1: H is a group that acts on a set Y
    try:
        H = witness['H']
        Y = list(witness['Y'])
        action_H_Y = witness['action_H_Y']
        
        H_elems = list(H.generate())
        H_id = H.identity
        
        h_acts_on_y = True
        for y in Y:
            if action_H_Y(H_id, y) != y:
                h_acts_on_y = False
                break
        if h_acts_on_y:
            for h in H_elems:
                for y in Y:
                    if action_H_Y(h, y) not in Y:
                        h_acts_on_y = False
                        break
                if not h_acts_on_y: break
        if h_acts_on_y:
            for h1 in H_elems:
                for h2 in H_elems:
                    for y in Y:
                        if action_H_Y(h1 * h2, y) != action_H_Y(h1, action_H_Y(h2, y)):
                            h_acts_on_y = False
                            break
                    if not h_acts_on_y: break
    except Exception:
        h_acts_on_y = False

    # neg_Q: G \times H does NOT act on X \times Y via the component-wise action
    try:
        if any(k not in witness for k in ('G', 'X', 'action_G_X', 'H', 'Y', 'action_H_Y')):
            neg_q = False
        else:
            G = witness['G']
            X = list(witness['X'])
            action_G_X = witness['action_G_X']
            
            try:
                G_elems = list(G.generate())
                G_id = G.identity
                
                g_acts = True
                for x in X:
                    if action_G_X(G_id, x) != x:
                        g_acts = False
                        break
                if g_acts:
                    for g in G_elems:
                        for x in X:
                            if action_G_X(g, x) not in X:
                                g_acts = False
                                break
                        if not g_acts: break
                if g_acts:
                    for g1 in G_elems:
                        for g2 in G_elems:
                            for x in X:
                                if action_G_X(g1 * g2, x) != action_G_X(g1, action_G_X(g2, x)):
                                    g_acts = False
                                    break
                            if not g_acts: break
                            
                # The component-wise action is valid if and only if both component actions are valid.
                gx_acts = g_acts and h_acts_on_y
                neg_q = not gx_acts
            except Exception:
                # If G is not a group or action_G_X raises an error, the action fails.
                neg_q = True
    except Exception:
        neg_q = False

    return [h_acts_on_y, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group that acts on a set Y",
    "¬Q: The direct product G x H does not act on X x Y via the component-wise action"
]

N_HYP = 1
NEG_Q_INDEX = 1