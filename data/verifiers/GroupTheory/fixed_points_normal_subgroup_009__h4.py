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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            X = witness.get('X', set(range(G.degree)) if hasattr(G, 'degree') else None)
            action = witness.get('action', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                X = set(range(G.degree)) if hasattr(G, 'degree') else None
                action = None
            elif len(witness) == 4:
                G, X, action, N = witness
            else:
                return [False] * 4 + [False]
        else:
            return [False] * 4 + [False]
    except Exception:
        return [False] * 4 + [False]

    def apply_action(g, x):
        if action is not None:
            if callable(action):
                return action(g, x)
            elif isinstance(action, dict):
                return action[(g, x)]
        return g(x)

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple))
        if h2:
            X = set(X)
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = False
        if h1 and h2:
            h3 = True
            # Check closure
            for g in G.generators:
                for x in X:
                    if apply_action(g, x) not in X:
                        h3 = False
                        break
                if not h3:
                    break
            
            # Check identity
            if h3:
                if G.generators:
                    g0 = G.generators[0]
                    e = g0 * (~g0)
                else:
                    e = Permutation(size=G.degree)
                
                for x in X:
                    if apply_action(e, x) != x:
                        h3 = False
                        break
                        
            # Check compatibility for generators
            if h3 and action is not None:
                for g1 in G.generators:
                    for g2 in G.generators:
                        g12 = g1 * g2
                        for x in X:
                            act1 = apply_action(g12, x)
                            act_left = apply_action(g1, apply_action(g2, x))
                            act_right = apply_action(g2, apply_action(g1, x))
                            if act1 != act_left and act1 != act_right:
                                h3 = False
                                break
                        if not h3:
                            break
    except Exception:
        h3 = False

    # H4: X^N is the set of points in X fixed by every element of N
    try:
        h4 = False
        if h1:
            if isinstance(N, PermutationGroup):
                h4 = all(g in G for g in N.generators)
                N_elements = list(N.generate())
            elif isinstance(N, (list, tuple, set)):
                h4 = all(g in G for g in N)
                N_elements = list(N)
    except Exception:
        h4 = False

    # neg_Q: The set X^N is not invariant under the action of G
    try:
        neg_q = False
        if h1 and h2 and h3 and h4:
            X_N = set()
            for x in X:
                if all(apply_action(n, x) == x for n in N_elements):
                    X_N.add(x)
            
            try:
                if G.order() < 1000:
                    elements_to_check = list(G.generate())
                else:
                    elements_to_check = G.generators
            except Exception:
                elements_to_check = G.generators
                
            for g in elements_to_check:
                for x in X_N:
                    if apply_action(g, x) not in X_N:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "H_4: X^N is the set of points in X fixed by every element of N",
    "¬Q: The set X^N is not invariant under the action of G"
]

N_HYP = 4
NEG_Q_INDEX = 4