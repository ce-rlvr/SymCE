import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
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
    """
    witness is expected to be a tuple: (G, X, Y, act_X, act_Y, x)
    where:
      - G is a group (e.g., a PermutationGroup or list of elements closed under *)
      - X is a list/set of elements
      - Y is a list/set of elements
      - act_X is a function (g, a) -> a' defining the action of G on X
      - act_Y is a function (g, b) -> b' defining the action of G on Y
      - x is an element of X
    """
    try:
        G, X, Y, act_X, act_Y, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group, and acts on X and Y
    h1 = False
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
        
        if len(elements) > 0:
            elements_set = set(elements)
            closed = True
            for g1 in elements:
                for g2 in elements:
                    if (g1 * g2) not in elements_set:
                        closed = False
                        break
                if not closed:
                    break
            
            if closed:
                valid_X = True
                X_set = set(X)
                for a in X:
                    for g in elements:
                        if act_X(g, a) not in X_set:
                            valid_X = False
                            break
                    if not valid_X: break
                
                if valid_X:
                    is_left = True
                    is_right = True
                    for a in X:
                        for g1 in elements:
                            for g2 in elements:
                                if act_X(g1, act_X(g2, a)) != act_X(g1 * g2, a):
                                    is_left = False
                                if act_X(g2, act_X(g1, a)) != act_X(g1 * g2, a):
                                    is_right = False
                    valid_X = is_left or is_right

                valid_Y = True
                Y_set = set(Y)
                for a in Y:
                    for g in elements:
                        if act_Y(g, a) not in Y_set:
                            valid_Y = False
                            break
                    if not valid_Y: break
                
                if valid_Y:
                    is_left = True
                    is_right = True
                    for a in Y:
                        for g1 in elements:
                            for g2 in elements:
                                if act_Y(g1, act_Y(g2, a)) != act_Y(g1 * g2, a):
                                    is_left = False
                                if act_Y(g2, act_Y(g1, a)) != act_Y(g1 * g2, a):
                                    is_right = False
                    valid_Y = is_left or is_right

                identities = [g for g in elements if all(g * h == h for h in elements)]
                if identities:
                    e = identities[0]
                    if all(act_X(e, a) == a for a in X) and all(act_Y(e, a) == a for a in Y):
                        h1 = valid_X and valid_Y
    except Exception:
        h1 = False

    # H2: G acts transitively on Y
    h2 = False
    try:
        if h1 and len(Y) > 0:
            h2 = True
            for y1 in Y:
                for y2 in Y:
                    reachable = False
                    for g in elements:
                        if act_Y(g, y1) == y2:
                            reachable = True
                            break
                    if not reachable:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: x is an element of X
    h3 = False
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # ¬Q: The diagonal action of G on X \times Y is transitive iff the stabilizer G_x acts transitively on Y is FALSE
    neg_q = False
    try:
        if h1 and h3:
            # Check if diagonal action is transitive
            diag_transitive = True
            if len(X) == 0 or len(Y) == 0:
                diag_transitive = False
            else:
                for x1 in X:
                    for y1 in Y:
                        for x2 in X:
                            for y2 in Y:
                                reachable = False
                                for g in elements:
                                    if act_X(g, x1) == x2 and act_Y(g, y1) == y2:
                                        reachable = True
                                        break
                                if not reachable:
                                    diag_transitive = False
                                    break
                            if not diag_transitive: break
                        if not diag_transitive: break
                    if not diag_transitive: break
            
            # Check if G_x acts transitively on Y
            Gx = [g for g in elements if act_X(g, x) == x]
            Gx_transitive = True
            if len(Y) == 0:
                Gx_transitive = False
            else:
                for y1 in Y:
                    for y2 in Y:
                        reachable = False
                        for g in Gx:
                            if act_Y(g, y1) == y2:
                                reachable = True
                                break
                        if not reachable:
                            Gx_transitive = False
                            break
                    if not Gx_transitive:
                        break
            
            # The conclusion is the equivalence, so its negation is that they are not equal
            neg_q = (diag_transitive != Gx_transitive)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on sets X and Y",
    "H_2: G acts transitively on Y",
    "H_3: x is an element of X",
    "¬Q: The equivalence (diagonal action is transitive iff G_x acts transitively on Y) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3