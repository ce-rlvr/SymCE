import itertools
from sympy.combinatorics import PermutationGroup, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup for standard algebra objects
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
    Checks if the witness is a valid counterexample to the false conjecture:
    "The action is faithful if and only if the intersection of Stab_G(x) over all x in X is {e}."
    """
    try:
        if len(witness) == 2:
            G, X_iter = witness
            X = list(X_iter)
            act = lambda g, x: g(x)
        elif len(witness) == 3:
            G, X_iter, act = witness
            X = list(X_iter)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
            identity = G.identity
        else:
            elements = list(G)
            identity = None
            for e in elements:
                if all(e * x == x for x in elements):
                    identity = e
                    break
        h1 = (identity is not None)
        if h1:
            for a in elements:
                has_inv = False
                for b in elements:
                    if a * b == identity and b * a == identity:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: G acts on X
    try:
        h2 = True
        for x in X:
            if act(identity, x) != x:
                h2 = False
                break
        if h2:
            for g1 in elements:
                for g2 in elements:
                    for x in X:
                        if act(g1, act(g2, x)) != act(g1 * g2, x):
                            h2 = False
                            break
    except Exception:
        h2 = False

    # ¬Q: The action is faithful if and only if the intersection of Stab_G(x) over all x in X is {e} (must FAIL)
    try:
        # An action is faithful if its kernel is trivial
        kernel = []
        for g in elements:
            if all(act(g, x) == x for x in X):
                kernel.append(g)
        faithful = (len(kernel) == 1 and kernel[0] == identity)
        
        # Intersection of Stab_G(x) over all x in X
        if len(X) == 0:
            # The intersection of an empty family of subsets is empty
            intersection = []
        else:
            intersection = list(elements)
            for x in X:
                stab_x = [g for g in elements if act(g, x) == x]
                intersection = [g for g in intersection if g in stab_x]
                
        intersection_is_e = (len(intersection) == 1 and intersection[0] == identity)
        
        # The conjecture claims faithful <==> intersection_is_e
        Q = (faithful == intersection_is_e)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "¬Q: The equivalence (faithful iff intersection of stabilizers is {e}) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2