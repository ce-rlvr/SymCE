import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import free_group

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

# A free group of rank 2 is a standard example of a group with an infinite commutator subgroup
try:
    F2 = free_group("x y")[0]
except Exception:
    F2 = None

def conditions(witness) -> list[bool]:
    # H_1: Let G be a group
    try:
        h1_ok = False
        if hasattr(witness, 'generators') and hasattr(witness, 'order'):
            h1_ok = True
        elif witness.__class__.__name__ in ['FreeGroup', 'FpGroup', 'PermutationGroup']:
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The commutator subgroup G' is NOT a finite group
    try:
        neg_q_ok = False
        if witness.__class__.__name__ == 'FreeGroup':
            # The commutator subgroup of a free group is infinite iff rank >= 2
            neg_q_ok = len(witness.generators) >= 2
        else:
            # Attempt to compute the derived subgroup directly
            if hasattr(witness, 'derived_subgroup'):
                D = witness.derived_subgroup()
                if hasattr(D, 'order'):
                    if callable(D.order):
                        order = D.order()
                    else:
                        order = D.order
                    neg_q_ok = (order == sympy.oo)
                elif hasattr(D, 'is_finite'):
                    neg_q_ok = not D.is_finite
            
            # Fallback for finitely presented groups with no relators (isomorphic to FreeGroup)
            if not neg_q_ok and witness.__class__.__name__ == 'FpGroup':
                if hasattr(witness, 'relators') and len(witness.relators) == 0:
                    neg_q_ok = len(witness.generators) >= 2
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The commutator subgroup G' is not finite"
]

N_HYP = 1
NEG_Q_INDEX = 1