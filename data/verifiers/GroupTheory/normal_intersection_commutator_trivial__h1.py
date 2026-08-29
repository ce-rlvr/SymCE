import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = AlternatingGroup(4)
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
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H1: N is a normal subgroup of G
    try:
        is_subgroup = True
        for gen in N.generators:
            if not G.contains(gen):
                is_subgroup = False
                break
        
        is_normal = is_subgroup
        if is_subgroup:
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * ~g):
                        is_normal = False
                        break
                if not is_normal:
                    break
        h1_ok = bool(is_normal)
    except Exception:
        h1_ok = False

    # H2: N \cap G' is the trivial subgroup
    try:
        G_prime = G.derived_subgroup()
        h2_ok = True
        
        try:
            n_elems = list(N.generate())
        except Exception:
            n_elems = list(N.elements)
            
        for n in n_elems:
            if not G_prime.contains(n):
                continue
            
            is_id = False
            if hasattr(n, 'is_Identity'):
                is_id = n.is_Identity
            else:
                is_id = all(n(i) == i for i in range(n.size))
                
            if not is_id:
                h2_ok = False
                break
        h2_ok = bool(h2_ok)
    except Exception:
        h2_ok = False

    # neg_Q: N is NOT contained in Z(G)
    try:
        in_center = True
        for n in N.generators:
            for g in G.generators:
                if n * g != g * n:
                    in_center = False
                    break
            if not in_center:
                break
        neg_q_ok = not in_center
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N \\cap G' is the trivial subgroup",
    "¬Q: N is not contained in the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2