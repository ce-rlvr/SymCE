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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            Y = witness.get('Y')
            XY = witness.get('XY')
            x = witness.get('x')
            action_X = witness.get('action_X')
            action_Y = witness.get('action_Y')
            action_XY = witness.get('action_XY')
            op = witness.get('op')
            identity = witness.get('identity')
        else:
            G = getattr(witness, 'G', None)
            X = getattr(witness, 'X', None)
            Y = getattr(witness, 'Y', None)
            XY = getattr(witness, 'XY', None)
            x = getattr(witness, 'x', None)
            action_X = getattr(witness, 'action_X', None)
            action_Y = getattr(witness, 'action_Y', None)
            action_XY = getattr(witness, 'action_XY', None)
            op = getattr(witness, 'op', None)
            identity = getattr(witness, 'identity', None)

        if op is None:
            op = lambda g1, g2: g1 * g2
            
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
        else:
            G_elements = list(G)
            
        if identity is None:
            if hasattr(G, 'identity'):
                identity = G.identity
            else:
                for g in G_elements:
                    try:
                        is_id = True
                        for h in G_elements:
                            if op(g, h) != h or op(h, g) != h:
                                is_id = False
                                break
                        if is_id:
                            identity = g
                            break
                    except Exception:
                        continue
                        
        X_list = list(X)
        Y_list = list(Y)
        XY_list = list(XY)
    except Exception:
        return [False] * 5

    def call_action(action, g, z):
        if isinstance(action, dict):
            return action[(g, z)]
        return action(g, z)

    def is_action(domain, action_func):
        try:
            for z in domain:
                if call_action(action_func, identity, z) != z:
                    return False
            for g1 in G_elements:
                for g2 in G_elements:
                    g12 = op(g1, g2)
                    for z in domain:
                        z1 = call_action(action_func, g2, z)
                        if z1 not in domain:
                            return False
                        z2 = call_action(action_func, g1, z1)
                        if z2 != call_action(action_func, g12, z):
                            return False
            return True
        except Exception:
            return False

    # H1: X and Y are disjoint sets
    try:
        try:
            h1 = set(X_list).isdisjoint(set(Y_list))
        except TypeError:
            h1 = True
            for e1 in X_list:
                if e1 in Y_list:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: G acts on X and G acts on Y
    try:
        h2 = is_action(X_list, action_X) and is_action(Y_list, action_Y)
    except Exception:
        h2 = False

    # H3: G acts on the disjoint union X \sqcup Y such that g \cdot z is defined by the action on X if z \in X, and by the action on Y if z \in Y
    try:
        h3_action = is_action(XY_list, action_XY)
        h3_compat = True
        for g in G_elements:
            for z in XY_list:
                try:
                    if z in X_list:
                        if call_action(action_XY, g, z) != call_action(action_X, g, z):
                            h3_compat = False
                    if z in Y_list:
                        if call_action(action_XY, g, z) != call_action(action_Y, g, z):
                            h3_compat = False
                except Exception:
                    h3_compat = False
        h3 = h3_action and h3_compat
    except Exception:
        h3 = False

    # H4: x is an element of X
    try:
        h4 = x in X_list
    except Exception:
        h4 = False

    # Conclusion: The stabilizer of x under the action of G on X \sqcup Y is equal to the stabilizer of x under the action of G on X.
    try:
        stab_XY = []
        for g in G_elements:
            try:
                if call_action(action_XY, g, x) == x:
                    stab_XY.append(g)
            except Exception:
                pass
                
        stab_X = []
        for g in G_elements:
            try:
                if call_action(action_X, g, x) == x:
                    stab_X.append(g)
            except Exception:
                pass
                
        try:
            neg_Q = set(stab_XY) != set(stab_X)
        except TypeError:
            def is_subset(l1, l2):
                return all(any(e1 == e2 for e2 in l2) for e1 in l1)
            neg_Q = not (is_subset(stab_XY, stab_X) and is_subset(stab_X, stab_XY))
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: X and Y are disjoint sets",
    "H_2: G acts on X and G acts on Y",
    "H_3: G acts on the disjoint union X \sqcup Y such that g \cdot z is defined by the action on X if z \in X, and by the action on Y if z \in Y",
    "H_4: x is an element of X",
    "¬Q: The stabilizer of x under the action of G on X \sqcup Y is NOT equal to the stabilizer of x under the action of G on X"
]

N_HYP = 4
NEG_Q_INDEX = 4