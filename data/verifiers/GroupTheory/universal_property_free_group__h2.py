import sympy
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        F, S, G, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group on a set S
    try:
        h1 = type(F).__name__ == 'FreeGroup' and set(S) == set(F.generators)
    except Exception:
        h1 = False
        
    # H_2: f is a function from S to G
    try:
        h2 = isinstance(f, dict) and set(f.keys()) == set(S)
        if h2:
            for v in f.values():
                in_G = False
                try:
                    if v in G:
                        in_G = True
                except Exception:
                    pass
                
                if not in_G:
                    try:
                        if hasattr(G, 'contains') and G.contains(v):
                            in_G = True
                    except Exception:
                        pass
                
                if not in_G:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # ¬Q: There does NOT exist a unique group homomorphism from F to G that extends f.
    # The universal property of free groups guarantees a unique homomorphism if and only if G is a group.
    # If G is not a group (e.g., just a set), the concept of a group homomorphism to G is invalid,
    # so no such homomorphism exists and the conclusion fails.
    try:
        is_group = hasattr(G, 'identity') or type(G).__name__ in [
            'PermutationGroup', 'FreeGroup', 'FpGroup', 'CyclicGroup', 
            'DihedralGroup', 'SymmetricGroup', 'AlternatingGroup'
        ]
        neg_q = not is_group
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group on a set S",
    "H_2: f is a function from S to G",
    "¬Q: There does not exist a unique group homomorphism from F to G that extends f"
]

N_HYP = 2
NEG_Q_INDEX = 2