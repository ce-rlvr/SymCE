import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Standard group theory objects
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

# Linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Custom objects for infinite groups to allow counterexamples
class InfAbelianGroup:
    def __init__(self, name):
        self.name = name
        self.is_abelian = True

    def __repr__(self):
        return f"InfAbelianGroup({self.name})"

    def has_subgroup(self, H):
        if not isinstance(H, InfAbelianGroup):
            return False
        if self.name == H.name:
            return True
        if H.name == "0":
            return True
        if self.name == "Q" and H.name == "Z":
            return True
        if self.name == "R" and H.name in ["Z", "Q"]:
            return True
        return False

    def quotient_is_finitely_generated(self, H):
        if not self.has_subgroup(H):
            return False
        if self.name == H.name:
            return True
        if self.name == "Z":
            return True
        if self.name in ["Q", "R"]:
            return False
        return True

Q_group = InfAbelianGroup("Q")
Z_group = InfAbelianGroup("Z")
R_group = InfAbelianGroup("R")
trivial_inf_group = InfAbelianGroup("0")

def check_is_abelian(G):
    if hasattr(G, 'is_abelian'):
        val = G.is_abelian
        return val() if callable(val) else val
    return False

def check_is_subgroup(H, G):
    if hasattr(H, 'is_subgroup'):
        val = H.is_subgroup
        return val(G) if callable(val) else val
    if hasattr(G, 'has_subgroup'):
        val = G.has_subgroup
        return val(H) if callable(val) else val
    return False

def check_quotient_is_fg(G, H):
    if hasattr(G, 'quotient_is_finitely_generated'):
        val = G.quotient_is_finitely_generated
        return val(H) if callable(val) else val
    # Fallback for SymPy finite groups
    if hasattr(G, 'order'):
        return True
    return True

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(check_is_abelian(G))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(check_is_subgroup(H, G))
    except Exception:
        h2 = False
        
    try:
        neg_q = not bool(check_quotient_is_fg(G, H))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: H is a subgroup of G",
    "¬Q: The quotient group G/H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2