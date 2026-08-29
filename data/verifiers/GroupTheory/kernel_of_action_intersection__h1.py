import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # H1: X is a set
    try:
        X = witness.X
        h1 = isinstance(X, (set, list, tuple))
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        G = witness.G
        action = witness.action
        h2 = True
        
        # Check closure of action
        for g in G:
            for x in X:
                if action(g, x) not in X:
                    h2 = False
                    break
            if not h2:
                break
                
        # Check action axioms if an operation is provided
        if h2 and hasattr(witness, 'op'):
            op = witness.op
            for g in G:
                for h in G:
                    for x in X:
                        if action(g, action(h, x)) != action(op(g, h), x):
                            h2 = False
                            break
                    if not h2:
                        break
            
            if h2:
                # Find identity
                identity = None
                for e in G:
                    if all(op(e, g) == g and op(g, e) == g for g in G):
                        identity = e
                        break
                # If identity exists, it must act trivially
                if identity is not None:
                    for x in X:
                        if action(identity, x) != x:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # neg_Q: The kernel of the action of G on X is NOT equal to the intersection of Stab_G(x) over all x in X.
    try:
        # Determine if G is a group.
        # If G is a group, the kernel of the action is a normal subgroup (a subset of G).
        # If G is a semigroup/monoid or just a set, the kernel of the action is a congruence relation (a subset of G x G).
        is_group = False
        if getattr(witness, 'is_group', False):
            is_group = True
        elif type(G).__name__ == 'PermutationGroup':
            is_group = True
        elif hasattr(witness, 'op'):
            op = witness.op
            identity = None
            for e in G:
                if all(op(e, g) == g and op(g, e) == g for g in G):
                    identity = e
                    break
            if identity is not None:
                has_inverses = True
                for g in G:
                    inv_found = False
                    for h in G:
                        if op(g, h) == identity and op(h, g) == identity:
                            inv_found = True
                            break
                    if not inv_found:
                        has_inverses = False
                        break
                if has_inverses:
                    is_group = True

        if is_group:
            # For a group, the kernel is exactly the intersection of stabilizers by definition.
            # Both are the subset {g in G | forall x in X, g.x = x}.
            neg_Q = False
        else:
            # For a semigroup/set, the kernel of the action (homomorphism to transformations) is a congruence relation.
            kernel = {(g, h) for g in G for h in G if all(action(g, x) == action(h, x) for x in X)}
            # The intersection of stabilizers is a subset of G.
            intersection = {g for g in G if all(action(g, x) == x for x in X)}
            
            # A subset of G x G is not equal to a subset of G (unless both are empty, which kernel never is since it's reflexive).
            neg_Q = (kernel != intersection)
            
    except Exception:
        neg_Q = False

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "¬Q: The kernel of the action is not equal to the intersection of stabilizers"
]

N_HYP = 2
NEG_Q_INDEX = 2