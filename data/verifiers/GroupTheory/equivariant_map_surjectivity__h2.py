import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard groups and matrices
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If G acts transitively on X and phi: X -> Y is G-equivariant, then phi is surjective."
    """
    try:
        G = witness['G']
        X_raw = witness['X']
        Y_raw = witness['Y']
        action_X_raw = witness['action_X']
        action_Y_raw = witness['action_Y']
        phi_raw = witness['phi']
    except Exception:
        return [False, False, False]
        
    # Helpers to support both callables and dictionaries/mappings
    def phi(x):
        try:
            return phi_raw(x)
        except TypeError:
            return phi_raw[x]

    def action_X(g, x):
        try:
            return action_X_raw(g, x)
        except TypeError:
            return action_X_raw[(g, x)]

    def action_Y(g, y):
        try:
            return action_Y_raw(g, y)
        except TypeError:
            return action_Y_raw[(g, y)]

    try:
        if G.order() > 500:
            return [False, False, False]
        G_elems = list(G.generate())
        if not G_elems:
            return [False, False, False]
            
        # Find the identity element of the group
        id_g = None
        h0 = G_elems[0]
        for g in G_elems:
            if g * h0 == h0:
                is_id = True
                for h in G_elems:
                    if g * h != h:
                        is_id = False
                        break
                if is_id:
                    id_g = g
                    break
        if id_g is None:
            return [False, False, False]
            
        # Extract unique elements to form sets X and Y
        X = []
        for x in X_raw:
            if x not in X:
                X.append(x)
                
        Y = []
        for y in Y_raw:
            if y not in Y:
                Y.append(y)
                
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting transitively on a set X
    h1_ok = False
    try:
        if len(X) > 0:
            valid_action_X = True
            # Check identity axiom
            for x in X:
                if action_X(id_g, x) != x:
                    valid_action_X = False
                    break
            # Check closure
            if valid_action_X:
                for g in G_elems:
                    for x in X:
                        if action_X(g, x) not in X:
                            valid_action_X = False
                            break
                    if not valid_action_X: break
            # Check compatibility axiom (allow either left or right action convention)
            if valid_action_X:
                is_left = True
                is_right = True
                for g1 in G_elems:
                    for g2 in G_elems:
                        g12 = g1 * g2
                        for x in X:
                            if action_X(g12, x) != action_X(g1, action_X(g2, x)):
                                is_left = False
                            if action_X(g12, x) != action_X(g2, action_X(g1, x)):
                                is_right = False
                            if not is_left and not is_right:
                                break
                        if not is_left and not is_right:
                            break
                    if not is_left and not is_right:
                        break
                if not (is_left or is_right):
                    valid_action_X = False
            
            # Check transitivity
            if valid_action_X:
                x0 = X[0]
                orbit = []
                for g in G_elems:
                    val = action_X(g, x0)
                    if val not in orbit:
                        orbit.append(val)
                if len(orbit) == len(X) and all(x in orbit for x in X):
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: phi: X -> Y is a G-equivariant map
    h2_ok = False
    try:
        if len(Y) > 0:
            valid_action_Y = True
            # Check identity axiom
            for y in Y:
                if action_Y(id_g, y) != y:
                    valid_action_Y = False
                    break
            # Check closure
            if valid_action_Y:
                for g in G_elems:
                    for y in Y:
                        if action_Y(g, y) not in Y:
                            valid_action_Y = False
                            break
                    if not valid_action_Y: break
            # Check compatibility axiom
            if valid_action_Y:
                is_left = True
                is_right = True
                for g1 in G_elems:
                    for g2 in G_elems:
                        g12 = g1 * g2
                        for y in Y:
                            if action_Y(g12, y) != action_Y(g1, action_Y(g2, y)):
                                is_left = False
                            if action_Y(g12, y) != action_Y(g2, action_Y(g1, y)):
                                is_right = False
                            if not is_left and not is_right:
                                break
                        if not is_left and not is_right:
                            break
                    if not is_left and not is_right:
                        break
                if not (is_left or is_right):
                    valid_action_Y = False
            
            if valid_action_Y:
                # Check that phi maps X into Y
                maps_to_Y = True
                for x in X:
                    if phi(x) not in Y:
                        maps_to_Y = False
                        break
                
                # Check equivariance: phi(g * x) == g * phi(x)
                if maps_to_Y:
                    equiv = True
                    for g in G_elems:
                        for x in X:
                            if phi(action_X(g, x)) != action_Y(g, phi(x)):
                                equiv = False
                                break
                        if not equiv: break
                    if equiv:
                        h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: phi is NOT surjective
    neg_q_ok = False
    try:
        image = []
        for x in X:
            val = phi(x)
            if val not in image:
                image.append(val)
        if any(y not in image for y in Y):
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: phi: X -> Y is a G-equivariant map",
    "¬Q: phi is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2