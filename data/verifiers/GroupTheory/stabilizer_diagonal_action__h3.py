import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G = witness["G"]
        X = list(witness["X"])
        Y = list(witness["Y"])
        action_X = witness["action_X"]
        action_Y = witness["action_Y"]
        action_XY = witness["action_XY"]
        x = witness["x"]
        y = witness["y"]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        elements = list(G.elements)
        # Limit size to prevent timeouts during action verification
        if len(elements) > 50:
            h1 = False
        else:
            id_g = G.identity
            h1 = (id_g in elements)
    except Exception:
        h1 = False
        elements = []
        id_g = None

    def is_action(G_elems, id_g, S, act):
        # Check identity
        for p in S:
            if act(id_g, p) != p: 
                return False
        # Check closure
        for g in G_elems:
            for p in S:
                if act(g, p) not in S: 
                    return False
        # Check compatibility
        for g1 in G_elems:
            for g2 in G_elems:
                for p in S:
                    if act(g1, act(g2, p)) != act(g1 * g2, p):
                        return False
        return True

    # H2: X and Y are sets on which G acts
    try:
        if h1 and len(X) * len(Y) <= 100:
            h2 = is_action(elements, id_g, X, action_X) and \
                 is_action(elements, id_g, Y, action_Y)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: (x, y) is an element of X \times Y
    try:
        h3 = (x in X) and (y in Y)
    except Exception:
        h3 = False

    # neg_Q: The stabilizer of (x, y) in G is NOT the intersection of the stabilizers G_x and G_y
    try:
        if h1 and h2 and h3:
            XY = list(itertools.product(X, Y))
            # The conclusion implicitly assumes an action on X \times Y.
            # If the provided action is invalid, the witness is malformed.
            if not is_action(elements, id_g, XY, action_XY):
                neg_q = False
            else:
                stab_xy = {g for g in elements if action_XY(g, (x, y)) == (x, y)}
                stab_x = {g for g in elements if action_X(g, x) == x}
                stab_y = {g for g in elements if action_Y(g, y) == y}
                stab_x_cap_y = stab_x.intersection(stab_y)
                
                neg_q = (stab_xy != stab_x_cap_y)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are sets on which G acts",
    "H_3: (x, y) is an element of X \\times Y",
    "¬Q: The stabilizer of (x, y) in G is not the intersection of the stabilizers G_x and G_y"
]

N_HYP = 3
NEG_Q_INDEX = 3