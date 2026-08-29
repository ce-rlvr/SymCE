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

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False]
        
    # H_1: x and y are elements of G
    try:
        h1 = (x in G) and (y in G)
    except Exception:
        h1 = False
        
    # ¬Q: x and y are conjugate in G if and only if they have the same cycle type (must fail)
    try:
        # Ensure permutations are padded to the same degree for safe comparison and multiplication
        deg = max(G.degree, x.size, y.size)
        
        def pad_perm(p, d):
            arr = p.array_form
            if len(arr) < d:
                arr = arr + list(range(len(arr), d))
            return Permutation(arr)
            
        x_pad = pad_perm(x, deg)
        y_pad = pad_perm(y, deg)
        
        # Check if they have the same cycle type
        same_cycle_type = (x_pad.cycle_structure == y_pad.cycle_structure)
        
        # Check if they are conjugate in G
        are_conjugate = False
        for g in G.elements:
            g_pad = pad_perm(g, deg)
            # Check both left-to-right and right-to-left conjugation conventions to be safe
            if g_pad * x_pad * ~g_pad == y_pad or ~g_pad * x_pad * g_pad == y_pad:
                are_conjugate = True
                break
                
        # The conclusion is an iff statement. Its negation is an XOR (not equivalent).
        neg_q = (are_conjugate != same_cycle_type)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "¬Q: x and y being conjugate in G is not equivalent to them having the same cycle type"
]

N_HYP = 1
NEG_Q_INDEX = 1