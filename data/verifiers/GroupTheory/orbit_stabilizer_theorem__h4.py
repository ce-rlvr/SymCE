import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, X, act, x = witness
            elif len(witness) == 3:
                G, X, x = witness
                act = lambda g, y: g(y)
            else:
                return [False, False, False, False]
        else:
            G = witness.G
            X = witness.X
            x = witness.x
            act = getattr(witness, 'act', lambda g, y: g(y))
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        elements = []
        if isinstance(G, PermutationGroup):
            if G.order() > 2000:
                return [False, False, False, False]
            elements = list(G.generate())
            iden = G.identity
            h1 = True
        elif hasattr(G, 'elements') and hasattr(G, 'identity'):
            elements = list(G.elements)
            iden = G.identity
            h1 = True
        elif hasattr(G, 'generate') and hasattr(G, 'identity'):
            elements = list(G.generate())
            iden = G.identity
            h1 = True
        else:
            h1 = False
            
        if h1 and len(elements) > 2000:
            h1 = False
    except Exception:
        h1 = False

    # H2: X is a finite set
    try:
        h2 = isinstance(X, (set, list, tuple))
        if h2:
            X_list = list(X)
            if len(X_list) > 2000:
                h2 = False
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = True
        if h1 and h2:
            # 1. Identity acts trivially
            for y in X_list:
                if act(iden, y) != y:
                    h3 = False
                    break
            # 2. Closure
            if h3:
                for g in elements:
                    for y in X_list:
                        if act(g, y) not in X_list:
                            h3 = False
                            break
                    if not h3: break
            # 3. Compatibility (allow either left or right action conventions)
            if h3:
                is_left = True
                is_right = True
                for g in elements:
                    for h in elements:
                        for y in X_list:
                            if is_left and act(g, act(h, y)) != act(g * h, y):
                                is_left = False
                            if is_right and act(h, act(g, y)) != act(g * h, y):
                                is_right = False
                        if not is_left and not is_right:
                            break
                    if not is_left and not is_right:
                        break
                if not is_left and not is_right:
                    h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: |G| != |Orb(x)| * |Stab(x)|
    try:
        if h1:
            orb = set()
            stab_count = 0
            for g in elements:
                res = act(g, x)
                if res == x:
                    stab_count += 1
                
                try:
                    orb.add(res)
                except TypeError:
                    if isinstance(res, list):
                        orb.add(tuple(res))
                    elif isinstance(res, set):
                        orb.add(frozenset(res))
                    elif isinstance(res, dict):
                        orb.add(frozenset(res.items()))
                    else:
                        orb.add(str(res))
            
            neg_q = (len(elements) != len(orb) * stab_count)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "H_3: G acts on X",
    "¬Q: |G| != |Orb(x)| * |Stab(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3