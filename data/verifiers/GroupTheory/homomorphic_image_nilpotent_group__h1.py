import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
            f = witness['f']
        else:
            G, H, f = witness
    except Exception:
        return [False, False, False]

    # H_1: f: G \to H is a group homomorphism
    try:
        G_elements = list(G.generate())
        H_elements = set(H.generate())
        
        if callable(f):
            f_map = {g: f(g) for g in G_elements}
        else:
            f_map = f
            
        h1_ok = True
        for g in G_elements:
            if g not in f_map or f_map[g] not in H_elements:
                h1_ok = False
                break
                
        if h1_ok:
            for x in G_elements:
                for y in G_elements:
                    if f_map[x * y] != f_map[x] * f_map[y]:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: G is a nilpotent group
    try:
        h2_ok = bool(G.is_nilpotent)
    except Exception:
        h2_ok = False

    # ¬Q: The image f(G) is NOT a nilpotent subgroup of H
    try:
        if callable(f):
            f_map = {g: f(g) for g in G.generators}
        else:
            f_map = f
            
        image_gens = [f_map[g] for g in G.generators if g in f_map]
        if not image_gens:
            # Fallback to identity if generators are empty or not mapped
            try:
                ident = list(H.generate())[0]**0
            except Exception:
                ident = Permutation()
            image_gens = [ident]
            
        image_G = PermutationGroup(image_gens)
        neg_q_ok = not bool(image_G.is_nilpotent)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f: G \\to H is a group homomorphism",
    "H_2: G is a nilpotent group",
    "¬Q: f(G) is not a nilpotent subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2