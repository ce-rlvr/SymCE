import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
import itertools
import functools
import math

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

F2, x, y = free_group("x, y")
F3, a, b, c = free_group("a, b, c")

class CommutatorSubgroup:
    """
    Represents the commutator subgroup [G, G] of a group G.
    """
    def __init__(self, group):
        self.group = group

def conditions(witness):
    try:
        F, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        is_free_group = False
        if F.__class__.__name__ == 'FreeGroup':
            is_free_group = True
        elif F.__class__.__name__ == 'FpGroup' and len(F.relators) == 0:
            is_free_group = True
    except Exception:
        is_free_group = False

    # H1: F is a finitely generated free group
    try:
        h1 = is_free_group and len(F.generators) >= 0
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of F
    try:
        if isinstance(H, CommutatorSubgroup):
            h2 = H.group == F
        elif isinstance(H, str) and H in ["commutator_subgroup", "derived_subgroup"]:
            h2 = hasattr(F, 'generators')
        else:
            iterator = iter(H)
            elements = []
            try:
                for _ in range(100):
                    elements.append(next(iterator))
            except StopIteration:
                pass
            h2 = all(g in F for g in elements)
    except Exception:
        h2 = False
        
    # neg_Q: H is NOT finitely generated
    try:
        if isinstance(H, CommutatorSubgroup):
            neg_q = is_free_group and len(F.generators) >= 2 and H.group == F
        elif isinstance(H, str) and H in ["commutator_subgroup", "derived_subgroup"]:
            neg_q = is_free_group and len(F.generators) >= 2
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finitely generated free group",
    "H_2: H is a subgroup of F",
    "¬Q: H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2