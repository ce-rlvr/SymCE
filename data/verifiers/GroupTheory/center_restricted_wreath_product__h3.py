import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

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
Z = 'Z'

def conditions(witness) -> list[bool]:
    """
    [H_1, H_2, neg_Q]
    Initial logic and parameters are validated.
    """
    try:
        w = witness if isinstance(witness, (list, tuple)) else (
            witness.get('A', trivial), 
            witness.get('B', trivial), 
            witness.get('W_center_trivial', True)
        )
        
        h1 = (w[0].order() > 1) if hasattr(w[0], 'order') else bool(w[0])
        h2 = w[1].is_infinite if hasattr(w[1], 'is_infinite') else (w[1] == 'Z')
        
        return [h1, h2, not bool(w[2])]
    except Exception:
        return [False, False, False]

CONDITION_LABELS: list[str] = [
    "H_1: A is a non-trivial group",
    "H_2: B is an infinite group",
    "¬Q: The center of W is not the trivial subgroup"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2