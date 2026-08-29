import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        G, H, phi = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            G_els = set(G.generate_dimino())
            H_els = set(H.generate_dimino())
            if callable(phi):
                phi_dict = {g: phi(g) for g in G_els}
            elif isinstance(phi, dict):
                phi_dict = phi
            else:
                phi_dict = None
                
            h1 = h1 and (phi_dict is not None)
            if h1:
                h1 = h1 and set(phi_dict.keys()) == G_els
                h1 = h1 and all(v in H_els for v in phi_dict.values())
    except Exception:
        h1 = False

    try:
        G_els = set(G.generate_dimino())
        H_els = set(H.generate_dimino())
        
        if callable(phi):
            phi_dict = {g: phi(g) for g in G_els}
        elif isinstance(phi, dict):
            phi_dict = phi
        else:
            raise ValueError("phi must be a dictionary or callable")
            
        e_G = next(g for g in G_els if g * g == g)
        e_H = next(h for h in H_els if h * h == h)
        
        values = list(phi_dict.values())
        is_injective = len(values) == len(set(values))
        
        ker_phi = {x for x, y in phi_dict.items() if y == e_H}
        ker_is_trivial = (ker_phi == {e_G})
        
        neg_q = bool(is_injective != ker_is_trivial)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups and phi is a function from G to H",
    "¬Q: phi is injective XOR ker(phi) == {e_G}"
]

N_HYP = 1
NEG_Q_INDEX = 1