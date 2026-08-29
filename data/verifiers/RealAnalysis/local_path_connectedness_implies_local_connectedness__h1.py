import sympy
from sympy import Reals, Rationals, Integers, FiniteSet, Interval, Union, Intersection, ProductSet
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Note: Since local path-connectedness mathematically implies local connectedness,
    no valid counterexample can exist (the conjecture is actually a true statement).
    This verifier evaluates the properties for standard representations of spaces.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            known_spaces = {
                "R": (True, False),
                "R^n": (True, False),
                "Q": (False, True),
                "Z": (True, False),
                "topologist_sine_curve": (False, True),
                "comb_space": (False, True),
                "broom_space": (False, True),
                "S^1": (True, False),
                "S^2": (True, False),
            }
            if witness in known_spaces:
                h1, neg_q = known_spaces[witness]
                
        elif isinstance(witness, sympy.Set):
            if witness == Rationals:
                h1 = False
                neg_q = True
            elif witness in (Reals, Integers):
                h1 = True
                neg_q = False
            elif isinstance(witness, (FiniteSet, Interval, Union, ProductSet)):
                # Standard simple subsets of R / R^n in sympy are locally path-connected
                # and locally connected.
                h1 = True
                neg_q = False
                
        elif hasattr(witness, "is_connected") or hasattr(witness, "vertices"):
            # If the witness is a graph-like object, it is locally path-connected
            # and locally connected.
            h1 = True
            neg_q = False
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is locally path-connected",
    "¬Q: X is not a locally connected topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1