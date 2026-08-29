import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
        H = list(H)
    except Exception:
        return [False, False, False]

    # Helper to extract elements from the group
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
    except Exception:
        elements = []

    # H_1: G is a cyclic group
    try:
        try:
            order = G.order()
        except TypeError:
            order = G.order
            
        h1 = False
        for g in elements:
            try:
                g_order = g.order()
            except TypeError:
                g_order = g.order
            if g_order == order:
                h1 = True
                break
    except Exception:
        h1 = False

    # H_2: phi is a group endomorphism of G
    try:
        if isinstance(phi, dict):
            domain_ok = set(phi.keys()) == set(elements)
            codomain_ok = all(v in elements for v in phi.values())
            homo_ok = all(phi[x*y] == phi[x]*phi[y] for x in elements for y in elements)
            h2 = domain_ok and codomain_ok and homo_ok
        elif callable(phi):
            codomain_ok = all(phi(v) in elements for v in elements)
            homo_ok = all(phi(x*y) == phi(x)*phi(y) for x in elements for y in elements)
            h2 = codomain_ok and homo_ok
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: phi(H) is not a subset of H
    try:
        neg_q = False
        for h in H:
            val = phi[h] if isinstance(phi, dict) else phi(h)
            if val not in H:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: phi is a group endomorphism of G",
    "¬Q: phi(H) is not a subset of H"
]

N_HYP = 2
NEG_Q_INDEX = 2