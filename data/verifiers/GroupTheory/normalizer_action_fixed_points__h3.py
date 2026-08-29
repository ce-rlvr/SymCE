import itertools
import functools
import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    elif isinstance(G, (list, set, tuple)):
        return list(G)
    else:
        return list(G)

def conditions(witness):
    # Parse witness
    if isinstance(witness, dict):
        G = witness.get('G')
        X = witness.get('X')
        action = witness.get('action')
        H = witness.get('H')
        N = witness.get('N', None)
    elif len(witness) == 5:
        G, X, action, H, N = witness
    elif len(witness) == 4:
        G, X, action, H = witness
        N = None
    elif len(witness) == 3:
        G, X, H = witness
        action = lambda g, x: g(x)
        N = None
    elif len(witness) == 2:
        G, H = witness
        X = list(range(G.degree)) if hasattr(G, 'degree') else []
        action = lambda g, x: g(x)
        N = None
    else:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    h1_ok = False
    try:
        g_elems = get_elements(G)
        if hasattr(G, 'identity'):
            id_g = G.identity
        else:
            id_g = None
            for g in g_elems:
                if all(g * h == h for h in g_elems):
                    id_g = g
                    break
        
        if id_g is not None:
            h1_ok = True
            # Check identity action
            for x in X:
                if action(id_g, x) != x:
                    h1_ok = False
                    break
            # Check associativity
            if h1_ok:
                for g1 in g_elems:
                    for g2 in g_elems:
                        for x in X:
                            if action(g1, action(g2, x)) != action(g1 * g2, x):
                                h1_ok = False
                                break
                        if not h1_ok: break
                    if not h1_ok: break
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    h2_ok = False
    try:
        g_elems = get_elements(G)
        h_elems = get_elements(H)
        if len(h_elems) > 0:
            h2_ok = True
            # Subset check
            for h in h_elems:
                if h not in g_elems:
                    h2_ok = False
                    break
            # Closure check
            if h2_ok:
                for h1 in h_elems:
                    for h2 in h_elems:
                        if h1 * h2 not in h_elems:
                            h2_ok = False
                            break
                    if not h2_ok: break
            # Inverse check
            if h2_ok:
                for h in h_elems:
                    if h**-1 not in h_elems:
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False

    # H_3: N_G(H) is the normalizer of H in G
    h3_ok = False
    expected_N = []
    try:
        g_elems = get_elements(G)
        h_elems = get_elements(H)
        
        for g in g_elems:
            is_in_N = True
            for h in h_elems:
                if g * h * g**-1 not in h_elems:
                    is_in_N = False
                    break
            if is_in_N:
                for h in h_elems:
                    if g**-1 * h * g not in h_elems:
                        is_in_N = False
                        break
            if is_in_N:
                expected_N.append(g)
                
        if N is None:
            h3_ok = True
        else:
            N_elems = get_elements(N)
            h3_ok = True
            for n in N_elems:
                if n not in expected_N:
                    h3_ok = False
                    break
            if h3_ok:
                for n in expected_N:
                    if n not in N_elems:
                        h3_ok = False
                        break
    except Exception:
        h3_ok = False

    # ¬Q: There exists n in N_G(H) and x in X^H such that n \cdot x is not in X^H
    neg_q = False
    try:
        X_H = []
        h_elems = get_elements(H)
        for x in X:
            is_fixed = True
            for h in h_elems:
                if action(h, x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                X_H.append(x)
                
        if N is None:
            N_elems = expected_N
        else:
            N_elems = get_elements(N)
            
        for n in N_elems:
            for x in X_H:
                nx = action(n, x)
                if nx not in X_H:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "H_3: N_G(H) is the normalizer of H in G",
    "¬Q: There exists n in N_G(H) and x in X^H such that n \cdot x is not in X^H"
]

N_HYP = 3
NEG_Q_INDEX = 3