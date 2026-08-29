import sympy
import sympy.combinatorics
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

class NonAmenableGroup:
    @property
    def is_amenable(self):
        return False
    def __str__(self):
        return "FreeGroup(2)"

try:
    from sympy.combinatorics import free_group
    F2 = free_group("a b")[0]
except ImportError:
    F2 = NonAmenableGroup()

def is_amenable(grp):
    """
    Check if a group is amenable.
    Finite groups and abelian groups are amenable.
    Free groups of rank >= 2 are not amenable.
    """
    if hasattr(grp, 'is_amenable'):
        val = grp.is_amenable
        if isinstance(val, bool):
            return val
        if callable(val):
            return val()
            
    class_name = type(grp).__name__
    
    if class_name == 'PermutationGroup':
        return True
        
    if class_name == 'FreeGroup':
        return len(grp.generators) < 2
        
    if class_name == 'FpGroup':
        if len(grp.relators) == 0:
            return len(grp.generators) < 2
        try:
            if grp.order() != sympy.oo:
                return True
        except Exception:
            pass
        try:
            if grp.is_abelian:
                return True
        except Exception:
            pass
            
    return False

def conditions(witness) -> list[bool]:
    # Witness should be a tuple of two groups: (G, H)
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is an amenable group
    try:
        h1_ok = bool(is_amenable(H))
    except Exception:
        h1_ok = False
        
    # ¬Q: G x H is NOT an amenable group
    # Mathematically, G x H is amenable iff both G and H are amenable.
    try:
        g_amenable = is_amenable(G)
        h_amenable = is_amenable(H)
        q_ok = g_amenable and h_amenable
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is an amenable group",
    "¬Q: G x H is not an amenable group"
]

N_HYP = 1
NEG_Q_INDEX = 1
