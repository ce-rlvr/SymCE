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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            phi = witness['phi']
        else:
            G, H, phi = witness
    except Exception:
        return [False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # neg_Q: The restriction of phi to Z(G) is not an isomorphism from Z(G) onto Z(H)
    try:
        def eval_phi(phi_map, x):
            if isinstance(phi_map, dict):
                return phi_map[x]
            elif callable(phi_map):
                return phi_map(x)
            elif isinstance(phi_map, list):
                for k, v in phi_map:
                    if k == x:
                        return v
                raise ValueError("x not found in phi")
            else:
                raise ValueError("phi must be a dict, callable, or list of tuples")

        # Verify phi is a well-defined map from G to H
        valid_map = True
        for g in G.elements:
            try:
                val = eval_phi(phi, g)
                if val not in H.elements:
                    valid_map = False
                    break
            except Exception:
                valid_map = False
                break
        
        if not valid_map:
            neg_q = False
        else:
            Z_G = [g for g in G.elements if all(g * x == x * g for x in G.elements)]
            Z_H = [h for h in H.elements if all(h * y == y * h for y in H.elements)]
            
            Q = True
            mapped_Z_G = []
            for z in Z_G:
                pz = eval_phi(phi, z)
                if pz not in Z_H:
                    Q = False
                mapped_Z_G.append(pz)
                
            if Q:
                for z1 in Z_G:
                    for z2 in Z_G:
                        if eval_phi(phi, z1 * z2) != eval_phi(phi, z1) * eval_phi(phi, z2):
                            Q = False
                            break
                    if not Q:
                        break
                            
            if Q:
                if len(set(mapped_Z_G)) != len(mapped_Z_G):
                    Q = False
                elif len(set(mapped_Z_G)) != len(Z_H):
                    Q = False
                else:
                    for h in Z_H:
                        if h not in mapped_Z_G:
                            Q = False
                            break
                            
            neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: The restriction of phi to Z(G) is not an isomorphism from Z(G) onto Z(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1