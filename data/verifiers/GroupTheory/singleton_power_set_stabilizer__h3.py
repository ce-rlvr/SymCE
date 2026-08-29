import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
    try:
        # Unpack witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                X = None
                action = None
                action_P = None
            elif len(witness) == 3:
                G, X, x = witness
                action = None
                action_P = None
            elif len(witness) == 4:
                G, X, action, x = witness
                action_P = None
            elif len(witness) == 5:
                G, X, action, action_P, x = witness
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            X = witness.get('X', None)
            action = witness.get('action', None)
            action_P = witness.get('action_P', None)
            if G is None or x is None:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        # H1: G is a group acting on a set X
        try:
            if hasattr(G, 'elements') and callable(G.elements):
                elements = list(G.elements())
            elif hasattr(G, 'elements'):
                elements = list(G.elements)
            elif hasattr(G, 'generate'):
                elements = list(G.generate())
            else:
                elements = list(G)
            h1 = len(elements) > 0
        except Exception:
            h1 = False

        # H2: P(X) is the power set of X
        h2 = True

        # H3: x is an element of X
        try:
            if X is not None:
                if hasattr(X, 'contains'):
                    h3 = bool(X.contains(x))
                else:
                    h3 = x in X
            else:
                if hasattr(G, 'degree') and isinstance(x, int):
                    h3 = 0 <= x < G.degree
                else:
                    h3 = True
        except Exception:
            h3 = False

        # Conclusion: stabilizer of {x} in P(X) == stabilizer of x in X
        try:
            def act(g, y):
                if action is not None:
                    return action(g, y)
                if hasattr(g, '__call__'):
                    return g(y)
                return g * y

            stab_x_indices = []
            stab_singleton_indices = []

            for i, g in enumerate(elements):
                try:
                    gx = act(g, x)
                except Exception:
                    continue
                
                # Check if g stabilizes x
                try:
                    is_eq = bool(gx == x)
                except Exception:
                    try:
                        is_eq = bool((gx == x).all())
                    except Exception:
                        is_eq = False
                
                if is_eq:
                    stab_x_indices.append(i)
                
                # Check if g stabilizes {x}
                if action_P is not None:
                    try:
                        singleton_x = {x}
                    except TypeError:
                        singleton_x = [x]
                    
                    try:
                        gx_set = action_P(g, singleton_x)
                        is_set_eq = bool(gx_set == singleton_x)
                    except Exception:
                        is_set_eq = False
                    
                    if is_set_eq:
                        stab_singleton_indices.append(i)
                else:
                    try:
                        is_set_eq = bool({gx} == {x})
                    except TypeError:
                        try:
                            is_set_eq = bool([gx] == [x])
                        except Exception:
                            is_set_eq = False
                    except Exception:
                        is_set_eq = False
                        
                    if is_set_eq:
                        stab_singleton_indices.append(i)

            neg_q = stab_x_indices != stab_singleton_indices
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: P(X) is the power set of X",
    "H_3: x is an element of X",
    "¬Q: The stabilizer of {x} in P(X) is not equal to the stabilizer of x in X"
]

N_HYP = 3
NEG_Q_INDEX = 3