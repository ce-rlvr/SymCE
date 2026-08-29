import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def extract_G_n(witness):
    if isinstance(witness, dict):
        return witness.get('G'), witness.get('n')
    elif isinstance(witness, tuple) and len(witness) == 2:
        if isinstance(witness[0], int) or (hasattr(witness[0], 'is_Integer') and witness[0].is_Integer):
            return witness[1], witness[0]
        else:
            return witness[0], witness[1]
    elif hasattr(witness, 'G') and hasattr(witness, 'n'):
        return witness.G, witness.n
    else:
        G = witness
        n = getattr(G, 'degree', None)
        return G, n

def is_center_trivial(G):
    try:
        C = G.center()
        try:
            order = C.order()
        except TypeError:
            order = C.order
        return int(order) == 1
    except Exception:
        pass
    
    gens = G.generators
    elements = list(G.generate())
    center_order = 0
    for g in elements:
        if all(g * h == h * g for h in gens):
            center_order += 1
    return center_order == 1

def conditions(witness) -> list[bool]:
    G, n = extract_G_n(witness)
    
    try:
        if isinstance(n, (int, sympy.Integer)) or (isinstance(n, float) and n.is_integer()):
            n_val = int(n)
            h1 = (n_val % 2 == 1) and (n_val > 1)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_center_trivial(G)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd integer greater than 1",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1
