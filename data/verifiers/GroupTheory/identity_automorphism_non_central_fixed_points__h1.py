import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, phi = witness
    except Exception:
        return [False, False, False]

    try:
        if not isinstance(G, PermutationGroup):
            return [False, False, False]
        
        try:
            elements = list(G.elements)
        except AttributeError:
            elements = list(G.generate())
            
        if callable(phi):
            phi_dict = {x: phi(x) for x in elements}
        elif isinstance(phi, dict):
            phi_dict = phi
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: phi is an automorphism of G
    try:
        h1 = False
        if len(phi_dict) == len(elements) and set(phi_dict.keys()) == set(elements) and set(phi_dict.values()) == set(elements):
            h1 = True
            for x in elements:
                for y in elements:
                    if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: For all x \in G \setminus Z(G), phi(x) = x
    try:
        h2 = False
        if h1:
            h2 = True
            try:
                center_elements = set(G.center().elements)
            except AttributeError:
                center_elements = set(G.center().generate())
                
            for x in elements:
                if x not in center_elements:
                    if phi_dict[x] != x:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: phi is not the identity automorphism
    try:
        neg_q = False
        if h1:
            for x in elements:
                if phi_dict[x] != x:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi is an automorphism of G",
    "H_2: For all x in G \\ Z(G), phi(x) = x",
    "¬Q: phi is not the identity automorphism on G"
]

N_HYP = 2
NEG_Q_INDEX = 2