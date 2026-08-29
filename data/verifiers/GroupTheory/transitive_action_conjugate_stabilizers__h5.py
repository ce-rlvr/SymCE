import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts transitively on X",
    "H_4: x is an element of X",
    "¬Q: There is no g in G such that Stab_G(y) = g * Stab_G(x) * g^{-1}"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        G, X, x, y = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple)) and all(isinstance(a, (int, sympy.Integer)) and a >= 0 for a in X)
    except Exception:
        h2 = False

    # H_3: G acts transitively on X
    try:
        if not (h1 and h2):
            h3 = False
        else:
            X_set = set(X)
            if not X_set:
                h3 = False
            else:
                invariant = True
                for gen in G.generators:
                    for a in X_set:
                        if gen(a) not in X_set:
                            invariant = False
                            break
                    if not invariant:
                        break
                if not invariant:
                    h3 = False
                else:
                    elem = next(iter(X_set))
                    orbit = set([elem])
                    queue = [elem]
                    while queue:
                        curr = queue.pop(0)
                        for gen in G.generators:
                            nxt = gen(curr)
                            if nxt not in orbit:
                                orbit.add(nxt)
                                queue.append(nxt)
                    h3 = (orbit == X_set)
    except Exception:
        h3 = False

    # H_4: x is an element of X
    try:
        h4 = h2 and (x in set(X))
    except Exception:
        h4 = False

    # neg_Q: There is no g in G such that Stab_G(y) = g * Stab_G(x) * g^{-1}
    try:
        if not h1:
            neg_q = False
        elif not isinstance(y, (int, sympy.Integer)) or y < 0:
            neg_q = False
        elif G.order() > 1000:
            neg_q = False
        else:
            stab_x = set()
            stab_y = set()
            elements = list(G.generate())
            for g in elements:
                if g(x) == x:
                    stab_x.add(g)
                if g(y) == y:
                    stab_y.add(g)
            
            neg_q = True
            for g in elements:
                conjugate_stab = set()
                for h in stab_x:
                    conjugate_stab.add(g * h * ~g)
                if conjugate_stab == stab_y:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]