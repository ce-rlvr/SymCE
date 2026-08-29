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

def get_Z_i(G, i):
    """
    Computes the i-th term of the upper central series of G.
    Returns a set of elements.
    """
    Z = {G.identity}
    elements = list(G.elements) if not callable(getattr(G, 'elements', None)) else list(G.elements())
    for _ in range(i):
        next_Z = set()
        for x in elements:
            # x is in Z_{k+1} iff for all y in G, [x, y] is in Z_k
            # [x, y] = x^-1 * y^-1 * x * y
            if all((x**-1 * y**-1 * x * y) in Z for y in elements):
                next_Z.add(x)
        # Optimization: if the series stabilizes, we can stop early
        if len(next_Z) == len(Z):
            break
        Z = next_Z
    return Z

def conditions(witness):
    try:
        G, H, i = witness
    except Exception:
        return [False, False]
        
    # H_1: i is a non-negative integer
    try:
        h1 = isinstance(i, int) and i >= 0
    except Exception:
        h1 = False
        
    # ¬Q: Z_i(G x H) != Z_i(G) x Z_i(H)
    try:
        GH = G * H
        Z_i_GH = get_Z_i(GH, i)
        Z_i_G = get_Z_i(G, i)
        Z_i_H = get_Z_i(H, i)
        
        if hasattr(G, 'degree') and hasattr(H, 'degree'):
            # For Sympy PermutationGroups, the direct product G * H has degree G.degree + H.degree.
            # We construct the direct product of the sets Z_i(G) and Z_i(H) to match Sympy's representation.
            Z_i_G_x_H = set()
            deg_G = G.degree
            deg_H = H.degree
            for g in Z_i_G:
                for h in Z_i_H:
                    arr_g = g.array_form
                    arr_g = arr_g + list(range(len(arr_g), deg_G))
                    arr_h = h.array_form
                    arr_h = arr_h + list(range(len(arr_h), deg_H))
                    arr_h_shifted = [x + deg_G for x in arr_h]
                    arr_combined = arr_g + arr_h_shifted
                    Z_i_G_x_H.add(Permutation(arr_combined))
        else:
            # Fallback for custom group objects where elements of G * H might be represented as tuples
            Z_i_G_x_H = {(g, h) for g in Z_i_G for h in Z_i_H}
            
        neg_q = (Z_i_GH != Z_i_G_x_H)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: i is a non-negative integer",
    "¬Q: Z_i(G x H) != Z_i(G) x Z_i(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1