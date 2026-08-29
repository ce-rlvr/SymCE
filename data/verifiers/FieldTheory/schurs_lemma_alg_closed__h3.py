import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix
from sympy import Rational, Integer
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        K = witness.get('K')
        G = witness.get('G')
        phi = witness.get('phi')
    except Exception:
        return [False, False, False, False]
    
    # H_1: K is an algebraically closed field
    try:
        h1 = K in ['CC', 'C', sympy.S.Complexes, 'AlgebraicallyClosedField']
    except Exception:
        h1 = False
        
    # H_2: G is a group
    matrices = []
    try:
        h2 = False
        if isinstance(G, list) and len(G) > 0:
            n = G[0].shape[0]
            h2 = True
            for g in G:
                if not hasattr(g, 'shape') or g.shape != (n, n):
                    h2 = False
                    break
            if h2:
                I = eye(n)
                if not any(g == I for g in G):
                    h2 = False
                else:
                    for g1 in G:
                        if not h2: break
                        for g2 in G:
                            if not any(g1 * g2 == g for g in G):
                                h2 = False
                                break
                    if h2:
                        for g in G:
                            if g.det() == 0:
                                h2 = False
                                break
                            inv = g.inv()
                            if not any(inv == h for h in G):
                                h2 = False
                                break
                if h2:
                    matrices = G
        else:
            elements = None
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif hasattr(G, 'generate'):
                elements = list(G.generate())
            
            if elements is not None:
                h2 = True
                rep = witness.get('rep')
                if rep is not None:
                    if isinstance(rep, dict):
                        get_rep = lambda g: rep.get(g, None)
                    elif callable(rep):
                        get_rep = rep
                    else:
                        get_rep = lambda g: None
                    
                    mats = []
                    valid_rep = True
                    for g in elements:
                        m = get_rep(g)
                        if m is None or not hasattr(m, 'shape') or m.shape[0] != m.shape[1]:
                            valid_rep = False
                            break
                        mats.append(m)
                    
                    if valid_rep and len(mats) > 0:
                        n = mats[0].shape[0]
                        I = eye(n)
                        for g1 in elements:
                            if not valid_rep: break
                            for g2 in elements:
                                if get_rep(g1 * g2) != get_rep(g1) * get_rep(g2):
                                    valid_rep = False
                                    break
                        if valid_rep:
                            for e in elements:
                                if e * e == e:
                                    if get_rep(e) != I:
                                        valid_rep = False
                                    break
                        if valid_rep:
                            matrices = mats
    except Exception:
        h2 = False

    # H_3: phi is a G-equivariant K-linear map from V to V
    try:
        h3 = False
        if matrices and phi is not None and hasattr(phi, 'shape'):
            n = matrices[0].shape[0]
            if phi.shape == (n, n):
                h3 = all(g * phi == phi * g for g in matrices)
    except Exception:
        h3 = False
        
    # ¬Q: phi is not a scalar multiple of the identity map
    try:
        neg_q = False
        if phi is not None and hasattr(phi, 'shape') and phi.shape[0] == phi.shape[1] and phi.shape[0] > 0:
            n = phi.shape[0]
            c = phi[0, 0]
            neg_q = bool(phi != c * eye(n))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: G is a group",
    "H_3: phi is a G-equivariant K-linear map from V to V",
    "¬Q: phi is not a scalar multiple of the identity map"
]

N_HYP = 3
NEG_Q_INDEX = 3