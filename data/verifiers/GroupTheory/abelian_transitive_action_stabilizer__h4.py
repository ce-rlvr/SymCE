import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if len(witness) == 2:
            G, X = witness
            action_func = lambda g, x: g(x)
        elif len(witness) == 3:
            G, X, action = witness
            if isinstance(action, dict):
                action_func = lambda g, x: action[(g, x)]
            else:
                action_func = action
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is an abelian group
    try:
        if hasattr(G, 'is_abelian'):
            h1 = bool(G.is_abelian)
            elements = list(G.generate())
            id_g = G.identity
        else:
            elements = list(G)
            h1 = all(a*b == b*a for a in elements for b in elements)
            id_g = next(g for g in elements if all(g*h == h for h in elements))
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (list, set, tuple, frozenset, sympy.Set))
    except Exception:
        h2 = False

    # Helper to check if X is empty
    try:
        is_empty = False
        try:
            if len(X) == 0:
                is_empty = True
        except Exception:
            if getattr(X, 'is_empty', False):
                is_empty = True
    except Exception:
        is_empty = False

    # H3: G acts transitively on X
    try:
        is_action = True
        if not is_empty:
            for x in X:
                if action_func(id_g, x) != x:
                    is_action = False
            
            is_left_action = True
            is_right_action = True
            for g1 in elements:
                for g2 in elements:
                    for x in X:
                        if action_func(g1, action_func(g2, x)) != action_func(g1*g2, x):
                            is_left_action = False
                        if action_func(g2, action_func(g1, x)) != action_func(g1*g2, x):
                            is_right_action = False
            if not (is_left_action or is_right_action):
                is_action = False
        
        is_transitive = True
        for x in X:
            for y in X:
                if not any(action_func(g, x) == y for g in elements):
                    is_transitive = False
                    break
            if not is_transitive:
                break
        h3 = is_action and is_transitive
    except Exception:
        h3 = False

    # neg_Q: The point stabilizer G_x is equal to the kernel of the action of G on X.
    try:
        if is_empty:
            # If X is empty, there is no point x, so "The point stabilizer G_x" is undefined.
            # Thus the statement "The point stabilizer G_x is equal to the kernel" is false.
            neg_q = True
        else:
            kernel = []
            for g in elements:
                if all(action_func(g, x) == x for x in X):
                    kernel.append(g)
            
            conclusion_holds = True
            for x in X:
                Gx = [g for g in elements if action_func(g, x) == x]
                if set(Gx) != set(kernel):
                    conclusion_holds = False
                    break
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: X is a set",
    "H_3: G acts transitively on X",
    "¬Q: The point stabilizer G_x is not equal to the kernel of the action (or is undefined)"
]

N_HYP = 3
NEG_Q_INDEX = 3