import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

# Custom classes and constants to support infinitely generated group witnesses
class InfiniteAbelianGroup:
    def __init__(self, name):
        self.name = name

    @property
    def is_nilpotent(self):
        return True

    @property
    def is_finitely_generated(self):
        return False

    def is_subgroup(self, other):
        if self == other:
            return True
        if isinstance(other, InfiniteAbelianGroup):
            return self.name == other.name
        return False

Q_group = InfiniteAbelianGroup("Q")
R_group = InfiniteAbelianGroup("R")

KNOWN_GROUPS = {
    "Q": {"is_nilpotent": True, "is_finitely_generated": False},
    "R": {"is_nilpotent": True, "is_finitely_generated": False},
    "C": {"is_nilpotent": True, "is_finitely_generated": False},
    "Q/Z": {"is_nilpotent": True, "is_finitely_generated": False},
    "Z[1/p]": {"is_nilpotent": True, "is_finitely_generated": False},
    "Z(p^infty)": {"is_nilpotent": True, "is_finitely_generated": False},
    "Z^infty": {"is_nilpotent": True, "is_finitely_generated": False},
    "Z": {"is_nilpotent": True, "is_finitely_generated": True},
}

KNOWN_SUBGROUPS = {
    ("R", "Q"),
    ("C", "R"),
    ("C", "Q"),
    ("Q", "Z"),
    ("R", "Z"),
    ("C", "Z"),
}

def get_group_props(G):
    if isinstance(G, str):
        return KNOWN_GROUPS.get(G, None)
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
            
        # H_1: G is a nilpotent group
        try:
            props = get_group_props(G)
            if props:
                h1 = props["is_nilpotent"]
            elif hasattr(G, "is_nilpotent"):
                h1 = G.is_nilpotent() if callable(G.is_nilpotent) else G.is_nilpotent
            else:
                h1 = False
        except Exception:
            h1 = False
            
        # H_2: H is a subgroup of G
        try:
            if isinstance(G, str) and isinstance(H, str):
                if G == H or (G, H) in KNOWN_SUBGROUPS:
                    h2 = True
                else:
                    h2 = False
            elif hasattr(H, "is_subgroup"):
                h2 = H.is_subgroup(G)
            elif G == H:
                h2 = True
            else:
                h2 = False
        except Exception:
            h2 = False
            
        # neg_Q: H is NOT finitely generated
        try:
            props = get_group_props(H)
            if props:
                fin_gen = props["is_finitely_generated"]
                neg_q = not fin_gen
            elif hasattr(H, "is_finitely_generated"):
                fin_gen = H.is_finitely_generated() if callable(H.is_finitely_generated) else H.is_finitely_generated
                neg_q = not fin_gen
            elif hasattr(H, "generators"):
                fin_gen = len(H.generators) < float('inf')
                neg_q = not fin_gen
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2