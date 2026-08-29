import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "¬Q: G is not finitely presented"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness) -> list[bool]:
    try:
        is_fp = False
        
        # Check if it's a known SymPy group type that is finitely presented
        if isinstance(witness, PermutationGroup):
            is_fp = True
        elif type(witness).__name__ in ['FpGroup', 'FreeGroup']:
            is_fp = True
        elif witness == sympy.S.Integers:
            is_fp = True
        else:
            # Any finite group is finitely presented
            try:
                if callable(getattr(witness, 'order', None)):
                    if witness.order() < float('inf'):
                        is_fp = True
                elif getattr(witness, 'is_finite', False):
                    is_fp = True
            except Exception:
                pass
            
            # Check if it explicitly has finite generators and relators
            if not is_fp:
                try:
                    gens = witness.generators
                    rels = witness.relators
                    if isinstance(gens, (list, tuple, set)) and isinstance(rels, (list, tuple, set)):
                        is_fp = True
                except Exception:
                    pass
                    
        # The conclusion is "G is finitely presented".
        # We want the negation of the conclusion to be True when the conclusion fails.
        neg_q = not is_fp
    except Exception:
        neg_q = False

    return [neg_q]