import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        if isinstance(witness, dict):
            X_raw = list(witness['X'])
            G_raw = list(witness['G'])
            action = witness['action']
            e = witness.get('e', None)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                X_raw, G_raw, action = witness
                e = None
            elif len(witness) == 4:
                X_raw, G_raw, action, e = witness
            else:
                return [False, False, False]
            X_raw = list(X_raw)
            G_raw = list(G_raw)
        elif hasattr(witness, 'elements') and hasattr(witness, 'degree'):
            X_raw = list(range(witness.degree))
            G_raw = list(witness.elements)
            action = lambda g, x: g(x)
            e = witness.identity
        else:
            X_raw = list(witness.X)
            G_raw = list(witness.G)
            action = witness.action
            e = getattr(witness, 'e', None)
            
        X = []
        for x in X_raw:
            if x not in X:
                X.append(x)
                
        G = []
        for g in G_raw:
            if g not in G:
                G.append(g)
    except Exception:
        return [False, False, False]

    # Find identity if not provided
    if e is None:
        for g in G:
            try:
                if all(action(g, x) == x for x in X):
                    e = g
                    break
            except Exception:
                continue

    # H1: X is a nonempty set
    try:
        h1 = len(X) > 0
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        h2 = True
        for g in G:
            for x in X:
                if action(g, x) not in X:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # Transitive
    try:
        transitive = True
        for x in X:
            for y in X:
                if not any(action(g, x) == y for g in G):
                    transitive = False
                    break
            if not transitive:
                break
    except Exception:
        transitive = False

    # Free (stabilizer of every point is trivial)
    try:
        if e is None:
            free = False
        else:
            free = True
            for x in X:
                stab = []
                for g in G:
                    if action(g, x) == x:
                        stab.append(g)
                
                is_trivial = True
                has_e = False
                for s in stab:
                    if s == e:
                        has_e = True
                    else:
                        is_trivial = False
                
                if not (is_trivial and has_e):
                    free = False
                    break
    except Exception:
        free = False

    # Regular (sharply transitive)
    try:
        regular = True
        for x in X:
            for y in X:
                count = sum(1 for g in G if action(g, x) == y)
                if count != 1:
                    regular = False
                    break
            if not regular:
                break
    except Exception:
        regular = False

    # Conclusion: Regular iff (Transitive and Free)
    try:
        q = (regular == (transitive and free))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a nonempty set",
    "H_2: G acts on X",
    "¬Q: Regular iff transitive and stabilizer of every point is trivial (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2