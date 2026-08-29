import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Standard finite groups
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

# Standard matrices
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Custom classes to represent infinite groups and subgroups,
# since SymPy lacks native support for infinitely generated groups.
class AbstractGroup:
    def __init__(self, name, is_fg):
        self.name = name
        self.is_finitely_generated = is_fg
        
    def __str__(self):
        return self.name

class AbstractSubgroup:
    def __init__(self, name, parent, is_fg):
        self.name = name
        self.parent = parent
        self.is_finitely_generated = is_fg
        
    def is_subgroup(self, G):
        return self.parent == G
        
    def __str__(self):
        return self.name

# Known counterexamples
F2 = AbstractGroup("F2", True)
F2_commutator = AbstractSubgroup("[F2, F2]", F2, False)

BS_1_2 = AbstractGroup("BS(1,2)", True)
BS_subgroup = AbstractSubgroup("Z[1/2]", BS_1_2, False)


def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is finitely generated
    try:
        if hasattr(G, 'is_finitely_generated'):
            h1 = bool(G.is_finitely_generated)
        elif hasattr(G, 'generators'):
            h1 = True  # SymPy permutation/Fp groups are finitely generated
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        if G == H:
            h2 = True
        elif hasattr(H, 'is_subgroup'):
            h2 = bool(H.is_subgroup(G))
        elif hasattr(H, 'is_subset'):
            h2 = bool(H.is_subset(G))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: H is NOT finitely generated
    try:
        if hasattr(H, 'is_finitely_generated'):
            neg_q = not bool(H.is_finitely_generated)
        elif hasattr(H, 'generators'):
            neg_q = False  # SymPy permutation/Fp groups are finitely generated
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]


CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "H_2: H is a subgroup of G",
    "¬Q: H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2