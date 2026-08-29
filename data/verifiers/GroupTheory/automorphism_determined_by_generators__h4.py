import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
        G, S, phi, psi = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: S is a generating set for G
    try:
        h2 = False
        if h1:
            if isinstance(S, (list, set, tuple)):
                if len(S) == 0:
                    if G.order() == 1:
                        h2 = True
                else:
                    H = PermutationGroup(list(S))
                    if H.order() == G.order() and all(G.contains(s) for s in S):
                        h2 = True
    except Exception:
        h2 = False

    # H_3: \phi and \psi are automorphisms of G
    try:
        h3 = False
        if h1:
            elements = list(G.elements)
            
            if callable(phi):
                phi_map = {g: phi(g) for g in elements}
            elif isinstance(phi, dict):
                phi_map = phi
            else:
                phi_map = {}
                
            if callable(psi):
                psi_map = {g: psi(g) for g in elements}
            elif isinstance(psi, dict):
                psi_map = psi
            else:
                psi_map = {}
            
            phi_is_auto = (set(phi_map.keys()) == set(elements) and 
                           set(phi_map.values()) == set(elements) and 
                           all(phi_map[g * h] == phi_map[g] * phi_map[h] for g in elements for h in elements))
                           
            psi_is_auto = (set(psi_map.keys()) == set(elements) and 
                           set(psi_map.values()) == set(elements) and 
                           all(psi_map[g * h] == psi_map[g] * psi_map[h] for g in elements for h in elements))
                           
            h3 = phi_is_auto and psi_is_auto
    except Exception:
        h3 = False

    # ¬Q: \phi(x) != \psi(x) for some x \in G
    try:
        neg_q = False
        if h1:
            elements = list(G.elements)
            
            if callable(phi):
                phi_map = {g: phi(g) for g in elements}
            elif isinstance(phi, dict):
                phi_map = phi
            else:
                phi_map = {}
                
            if callable(psi):
                psi_map = {g: psi(g) for g in elements}
            elif isinstance(psi, dict):
                psi_map = psi
            else:
                psi_map = {}
                
            if set(phi_map.keys()) == set(elements) and set(psi_map.keys()) == set(elements):
                neg_q = any(phi_map[g] != psi_map[g] for g in elements)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: S is a generating set for G",
    "H_3: phi and psi are automorphisms of G",
    "¬Q: phi(x) != psi(x) for some x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3