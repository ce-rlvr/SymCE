import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        # A valid witness must be a group. We check for the 'generators' attribute
        # which is present on SymPy's PermutationGroup, FpGroup, FreeGroup, etc.
        if not hasattr(witness, 'generators'):
            return [False]

        is_iso = False
        
        # SL(2, Z) is an infinite group. Any finite group is not isomorphic to it.
        if isinstance(witness, PermutationGroup):
            is_iso = False
        elif getattr(witness, 'is_finite', False):
            is_iso = False
        # If the witness is an FpGroup (has relators), we conservatively check if it 
        # has 2 generators. If it does, it might be SL(2, Z), so we assume it is 
        # to avoid falsely accepting it as a counterexample.
        elif hasattr(witness, 'relators'):
            if len(witness.generators) == 2:
                is_iso = True
            else:
                is_iso = False
        else:
            is_iso = False
            
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is not isomorphic to the group defined by the presentation < S, T | S^4 = 1, S^2 = (ST)^3 >"
]

N_HYP = 0
NEG_Q_INDEX = 0