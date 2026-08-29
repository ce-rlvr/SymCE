import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3), Permutation(0, 3)(1, 2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            x = witness.get('x')
            action = witness.get('action')
            Orb = witness.get('Orb')
            Stab = witness.get('Stab')
        elif len(witness) == 4:
            G, X, x, action = witness
            Orb = Stab = None
        elif len(witness) == 5:
            G, X, x, Orb, Stab = witness
            action = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'elements') or hasattr(G, 'order'):
            h1 = True
        elif isinstance(G, (list, tuple, set)):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: X is a finite set
    try:
        X_list = list(X)
        h2 = True
    except Exception:
        h2 = False
        X_list = []

    # H3: x \in X
    try:
        h3 = False
        for item in X_list:
            if item == x:
                h3 = True
                break
    except Exception:
        h3 = False

    # neg_Q: |G| != |Orb(x)| * |Stab(x)|
    try:
        if callable(action):
            act = action
        elif isinstance(action, dict):
            act = lambda g, pt: action[(g, pt)]
        else:
            act = None
            
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        if hasattr(G, 'order'):
            if callable(G.order):
                order = G.order()
            else:
                order = G.order
        else:
            order = len(elements)
            
        if act is not None:
            orb = []
            stab_count = 0
            for g in elements:
                y = act(g, x)
                found = False
                for item in orb:
                    if item == y:
                        found = True
                        break
                if not found:
                    orb.append(y)
                if y == x:
                    stab_count += 1
            neg_q = order != len(orb) * stab_count
        elif Orb is not None and Stab is not None:
            neg_q = order != len(list(Orb)) * len(list(Stab))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "H_3: x in X",
    "¬Q: |G| != |Orb(x)| * |Stab(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3