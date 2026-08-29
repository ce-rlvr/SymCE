import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)
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
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            A = witness.get('A')
            B = witness.get('B')
        else:
            G, H, f, A, B = witness
    except Exception:
        return [False, False]

    def get_elts(group):
        if hasattr(group, 'elements'):
            return list(group.elements)
        elif hasattr(group, 'generate'):
            return list(group.generate())
        else:
            return list(group)

    try:
        G_elts = get_elts(G)
        H_elts = get_elts(H)
        
        if callable(f):
            f_map = {g: f(g) for g in G_elts}
        elif isinstance(f, (list, tuple)):
            f_map = dict(f)
        else:
            f_map = f
            
        h1_ok = True
        
        # Check if f maps G to H
        for g in G_elts:
            if g not in f_map:
                h1_ok = False
                break
            if f_map[g] not in H_elts:
                h1_ok = False
                break
                
        # Check homomorphism property
        if h1_ok:
            for x in G_elts:
                for y in G_elts:
                    if f_map[x * y] != f_map[x] * f_map[y]:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
                    
        # Check injectivity
        if h1_ok:
            values = [f_map[g] for g in G_elts]
            if len(set(values)) != len(values):
                h1_ok = False
                
    except Exception:
        h1_ok = False

    try:
        def get_set(obj):
            if hasattr(obj, 'elements') or hasattr(obj, 'generate'):
                return set(get_elts(obj))
            return set(obj)
            
        A_set = get_set(A)
        B_set = get_set(B)
        
        # Ensure A and B are subsets of G
        if not A_set.issubset(set(G_elts)) or not B_set.issubset(set(G_elts)):
            neg_q_ok = False
        else:
            intersection_AB = A_set.intersection(B_set)
            image_intersection = {f_map[x] for x in intersection_AB}
            
            image_A = {f_map[x] for x in A_set}
            image_B = {f_map[x] for x in B_set}
            intersection_images = image_A.intersection(image_B)
            
            # The conclusion is f(A ∩ B) == f(A) ∩ f(B)
            # The negated conclusion is that they are NOT equal
            neg_q_ok = (image_intersection != intersection_images)
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is an injective group homomorphism from G to H",
    "¬Q: f(A ∩ B) != f(A) ∩ f(B)"
]

N_HYP = 1
NEG_Q_INDEX = 1