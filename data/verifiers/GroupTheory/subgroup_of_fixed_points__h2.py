import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, phi = witness
    except Exception:
        return [False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # neg_Q: The set S = {x \in G | \phi(x) = x} is NOT a subgroup of G
    try:
        elements = list(G.elements) if hasattr(G, 'elements') else list(G.generate())
        
        if isinstance(phi, dict):
            S = set(x for x in elements if phi.get(x, object()) == x)
        else:
            S = set(x for x in elements if phi(x) == x)
            
        is_subgroup = True
        if not S:
            is_subgroup = False
        else:
            # Check closure under group operation
            for x in S:
                for y in S:
                    if x * y not in S:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            
            # Check if identity is in S
            if is_subgroup:
                e = next(g for g in elements if g * g == g)
                if e not in S:
                    is_subgroup = False
                    
        neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The set S = {x in G | phi(x) = x} is not a subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1