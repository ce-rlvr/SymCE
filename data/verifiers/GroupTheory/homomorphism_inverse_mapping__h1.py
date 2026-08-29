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
        G = witness['G']
        H = witness['H']
        f = witness['f']
        x = witness['x']
    except Exception:
        return [False, False, False]

    # H_1: f: G \to H is a group homomorphism
    try:
        h1 = True
        G_elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        H_elements = list(H.elements) if hasattr(H, 'elements') else list(H)
        
        if callable(f):
            f_map = {g: f(g) for g in G_elements}
        else:
            f_map = f
            
        for g in G_elements:
            if g not in f_map:
                h1 = False
                break
            if f_map[g] not in H_elements:
                h1 = False
                break
                
        if h1:
            for a in G_elements:
                for b in G_elements:
                    if f_map[a * b] != f_map[a] * f_map[b]:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: x is an element of G
    try:
        G_elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        h2 = x in G_elements
    except Exception:
        h2 = False

    # neg_Q: f(x^{-1}) != (f(x))^{-1}
    try:
        try:
            x_inv = x**-1
        except Exception:
            x_inv = ~x
            
        if callable(f):
            fx = f(x)
            fx_inv_val = f(x_inv)
        else:
            fx = f[x]
            fx_inv_val = f[x_inv]
            
        try:
            expected_inv = fx**-1
        except Exception:
            expected_inv = ~fx
            
        neg_q = bool(fx_inv_val != expected_inv)
    except Exception:
        # If inverses cannot be computed or evaluated, the equality fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f: G \\to H is a group homomorphism",
    "H_2: x is an element of G",
    "¬Q: f(x^{-1}) != (f(x))^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2