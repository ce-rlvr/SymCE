import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

class ModuleWitness:
    """
    A mock class to represent an R-module for the purpose of this verifier,
    since SymPy does not have built-in support for abstract module theory, Supp(M), or Ann(M).
    """
    def __init__(self, is_finitely_generated: bool, supp_equals_v_ann: bool):
        self.is_finitely_generated = is_finitely_generated
        self.supp_equals_v_ann = supp_equals_v_ann

# Standard algebra objects
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
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_finitely_generated", False))
        else:
            h1 = bool(witness.is_finitely_generated)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get("supp_equals_v_ann", True))
        else:
            neg_q = not bool(witness.supp_equals_v_ann)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "¬Q: Supp(M) is not equal to the set of prime ideals of R containing Ann(M)"
]

N_HYP = 1
NEG_Q_INDEX = 1