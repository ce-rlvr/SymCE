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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, X, action = witness
        else:
            G = witness.G
            X = witness.X
            action = witness.action
        X = list(X)
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        if hasattr(G, 'is_group') and G.is_group:
            h1 = True
            elements = list(G.generate()) if hasattr(G, 'generate') else list(G)
            identity = G.identity if hasattr(G, 'identity') else None
            if identity is None:
                for e in elements:
                    if all(e * g == g for g in elements):
                        identity = e
                        break
        else:
            elements = list(G)
            h1 = False
            for e in elements:
                is_id = True
                for g in elements:
                    try:
                        if e * g != g or g * e != g:
                            is_id = False
                            break
                    except Exception:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    h1 = True
                    break
            
            if h1:
                for g in elements:
                    has_inv = False
                    for h in elements:
                        if g * h == identity and h * g == identity:
                            has_inv = True
                            break
                    if not has_inv:
                        h1 = False
                        break
                for g in elements:
                    for h in elements:
                        if g * h not in elements:
                            h1 = False
                            break
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False]

    # H2: G acts on X
    try:
        h2 = True
        for x in X:
            if action(identity, x) != x:
                h2 = False
                break
        
        if h2:
            for g in elements:
                for h in elements:
                    for x in X:
                        if action(g, action(h, x)) != action(g * h, x):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
                
        if h2:
            for g in elements:
                for x in X:
                    if action(g, x) not in X:
                        h2 = False
                        break
                if not h2: break
    except Exception:
        h2 = False

    # neg_Q: The kernel of the action is not equal to the intersection of Stab_G(x) over all x in X
    try:
        kernel = []
        for g in elements:
            if all(action(g, x) == x for x in X):
                if g not in kernel:
                    kernel.append(g)
                    
        if not X:
            # The intersection of an empty family of subsets of G is the universal class,
            # which is not equal to the kernel (a well-defined subset of G).
            intersection = "Universe"
            neg_q = True
        else:
            stabs = []
            for x in X:
                stab = []
                for g in elements:
                    if action(g, x) == x and g not in stab:
                        stab.append(g)
                stabs.append(stab)
                
            intersection = []
            for g in stabs[0]:
                if all(g in stab for stab in stabs[1:]):
                    intersection.append(g)
                    
            neg_q = False
            for g in kernel:
                if g not in intersection:
                    neg_q = True
                    break
            if not neg_q:
                for g in intersection:
                    if g not in kernel:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "¬Q: The kernel of the action is not equal to the intersection of stabilizers"
]

N_HYP = 2
NEG_Q_INDEX = 2