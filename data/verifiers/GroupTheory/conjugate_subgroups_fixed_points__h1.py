import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        G = witness['G']
        H = witness['H']
        g = witness['g']
        X = witness['X']
        action = witness['action']
    except Exception:
        return [False, False, False, False]

    def in_G(elem):
        try:
            if elem in G:
                return True
        except Exception:
            pass
        try:
            if hasattr(G, 'contains') and G.contains(elem):
                return True
        except Exception:
            pass
        return False

    # H_1: H is a subgroup of G
    try:
        if hasattr(G, 'identity'):
            identity = G.identity
        else:
            identity = None
            for e in G:
                if all(e * x == x for x in G):
                    identity = e
                    break
                    
        if hasattr(H, 'is_subgroup') and hasattr(H, 'elements'):
            h1 = H.is_subgroup(G)
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
            h1 = True
            for h in H_elems:
                if not in_G(h):
                    h1 = False
            if identity is not None and identity not in H_elems:
                h1 = False
            for h_a in H_elems:
                if h_a**-1 not in H_elems:
                    h1 = False
                for h_b in H_elems:
                    if h_a * h_b not in H_elems:
                        h1 = False
    except Exception:
        h1 = False
        H_elems = []

    # H_2: g is an element of G
    try:
        h2 = in_G(g)
    except Exception:
        h2 = False

    # H_3: gHg^{-1} is the conjugate subgroup of H by g
    try:
        g_inv = g**-1
        expected_gHg_inv = set(g * h * g_inv for h in H_elems)
        if 'gHg_inv' in witness:
            provided = set(witness['gHg_inv'])
            h3 = (provided == expected_gHg_inv)
            gHg_inv = provided
        else:
            gHg_inv = expected_gHg_inv
            h3 = True
    except Exception:
        h3 = False
        gHg_inv = set()

    # ¬Q: X^H and X^{gHg^{-1}} do not have the same cardinality
    try:
        def act(elem, x):
            if callable(action):
                return action(elem, x)
            elif isinstance(action, dict):
                return action[(elem, x)]
            else:
                raise ValueError("action must be callable or dict")
                
        X_H = []
        for x in X:
            fixed = True
            for h in H_elems:
                if act(h, x) != x:
                    fixed = False
                    break
            if fixed:
                X_H.append(x)
                
        X_gHg_inv = []
        for x in X:
            fixed = True
            for k in gHg_inv:
                if act(k, x) != x:
                    fixed = False
                    break
            if fixed:
                X_gHg_inv.append(x)
                
        neg_q = len(X_H) != len(X_gHg_inv)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: g is an element of G",
    "H_3: gHg^{-1} is the conjugate subgroup of H by g",
    "¬Q: X^H and X^{gHg^{-1}} do not have the same cardinality"
]

N_HYP = 3
NEG_Q_INDEX = 3