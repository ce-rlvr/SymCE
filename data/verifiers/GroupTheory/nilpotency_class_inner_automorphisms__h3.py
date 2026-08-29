import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: G is a nilpotent group
    try:
        h1 = bool(witness.is_nilpotent)
    except Exception:
        h1 = False

    # H_2: The nilpotency class of G is c, where c >= 1
    try:
        c = witness.nilpotency_class
        h2 = bool(c is not None and c >= 1)
    except Exception:
        h2 = False

    # ¬Q: Inn(G) is not a nilpotent group of class c-1
    try:
        if not h1 or not h2:
            c = witness.nilpotency_class
            if c is None:
                c = 1

        # Generate all elements of G to construct the regular representation of Inn(G)
        elements = []
        for i, e in enumerate(witness.generate()):
            if i > 2000:
                raise ValueError("Group too large to evaluate quickly")
            elements.append(e)
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        inn_gens = []
        
        # Each generator g of G induces an inner automorphism: x -> g * x * g^-1
        for g in witness.generators:
            perm = []
            for x in elements:
                y = g * x * ~g
                perm.append(elem_to_idx[y])
            inn_gens.append(Permutation(perm))
            
        # Ensure we have at least one generator (e.g., for the trivial group)
        if not inn_gens:
            size = len(elements)
            inn_gens.append(Permutation(size - 1 if size > 0 else 0))
            
        Inn_G = PermutationGroup(inn_gens)
        
        inn_is_nilp = Inn_G.is_nilpotent
        inn_c = Inn_G.nilpotency_class
        
        if inn_c is None:
            q = False
        else:
            q = inn_is_nilp and (inn_c == c - 1)
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: The nilpotency class of G is c, where c >= 1",
    "¬Q: Inn(G) is not a nilpotent group of class c-1"
]

N_HYP = 2
NEG_Q_INDEX = 2