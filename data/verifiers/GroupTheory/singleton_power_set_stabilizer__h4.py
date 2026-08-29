import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that x must be an element of X.
    """
    try:
        # Witness can be (G, X, x) with default action g(y), or (G, X, action, x)
        if len(witness) == 3:
            G, X, x = witness
            action = lambda g, y: g(y)
        elif len(witness) == 4:
            G, X, action, x = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
    except Exception:
        return [False, False, False, False]

    try:
        X_list = list(X)
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = True
        if not elements:
            h1 = False
        else:
            # Check closure of the action on X
            for g in elements:
                for y in X_list:
                    if action(g, y) not in X_list:
                        h1 = False
                        break
                if not h1:
                    break
            
            # Check existence of an identity element for the action
            if h1:
                has_id = False
                for g in elements:
                    if all(action(g, y) == y for y in X_list):
                        has_id = True
                        break
                if not has_id:
                    h1 = False
    except Exception:
        h1 = False

    # H_2: P(X) is the power set of X
    # This is a definitional hypothesis; it holds if the base setup is valid.
    h2 = h1

    # H_3: G acts on P(X) via the induced action
    # This is also definitional and follows from H_1.
    h3 = h1

    # Conclusion: The stabilizer of the singleton set {x} in the action on P(X) 
    # is equal to the stabilizer of x in the action on X.
    try:
        if x not in X_list:
            # If x is not in X, {x} is not a subset of X, so {x} is not in P(X).
            # The stabilizer of {x} in P(X) is undefined, as is the stabilizer of x in X.
            # The statement asserts equality of two well-defined stabilizers, which fails.
            q = False
        else:
            stab_x = []
            stab_set_x = []
            for g in elements:
                # Stabilizer of x in X
                if action(g, x) == x:
                    stab_x.append(g)
                
                # Stabilizer of {x} in P(X) via induced action
                g_S = [action(g, s) for s in [x]]
                if g_S[0] == x:
                    stab_set_x.append(g)
            
            q = (stab_x == stab_set_x)
    except Exception:
        q = False

    neg_q = not q

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: P(X) is the power set of X",
    "H_3: G acts on P(X) via the induced action",
    "¬Q: The stabilizer of {x} in P(X) is not equal to the stabilizer of x in X (e.g. undefined)"
]

N_HYP = 3
NEG_Q_INDEX = 3