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
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
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
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            action = witness['action']
        else:
            G, X, action = witness
    except Exception:
        try:
            G = witness.G
            X = witness.X
            action = witness.action
        except Exception:
            return [False, False, False]

    # H1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'is_group') and G.is_group:
            h1 = True
        elif isinstance(G, (list, set, tuple)) and len(G) > 0:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple))
    except Exception:
        h2 = False

    # neg_Q: The equivalence between faithful action and intersection of stabilizers being {e} fails
    try:
        if isinstance(G, PermutationGroup):
            G_elements = list(G.generate())
        elif hasattr(G, 'elements'):
            G_elements = list(G.elements)
        else:
            G_elements = list(G)

        e = None
        if hasattr(G, 'identity'):
            e = G.identity
        else:
            for g in G_elements:
                if isinstance(g, Permutation) and g.is_Identity:
                    e = g
                    break
            if e is None:
                if 0 in G_elements: e = 0
                elif 1 in G_elements: e = 1
                elif 'e' in G_elements: e = 'e'
                else: e = G_elements[0]

        def act(g, x):
            if callable(action):
                return action(g, x)
            elif isinstance(action, dict):
                return action[(g, x)]
            else:
                raise ValueError("Unknown action type")

        # A map G -> Sym(X) is faithful (injective) if no two distinct elements act identically
        faithful = True
        for g1 in G_elements:
            for g2 in G_elements:
                if g1 != g2:
                    same_action = True
                    for x in X:
                        if act(g1, x) != act(g2, x):
                            same_action = False
                            break
                    if same_action:
                        faithful = False
                        break
            if not faithful:
                break
        
        # Intersection of Stab_G(x) over all x in X
        intersection = []
        for g in G_elements:
            fixes_all = True
            for x in X:
                if act(g, x) != x:
                    fixes_all = False
                    break
            if fixes_all:
                intersection.append(g)
        
        is_only_e = True
        if len(intersection) == 0:
            is_only_e = False
        else:
            for g in intersection:
                if g != e:
                    is_only_e = False
                    break
        intersection_is_e = is_only_e
        
        # The conclusion fails if the equivalence does not hold
        neg_q = (faithful != intersection_is_e)

    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "¬Q: The equivalence between faithful action and intersection of stabilizers being {e} fails"
]

N_HYP = 2
NEG_Q_INDEX = 2