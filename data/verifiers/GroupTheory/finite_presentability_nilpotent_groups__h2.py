import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Since SymPy does not natively support non-finitely presented groups, this verifier
    relies on explicit attributes (e.g., on a mock object) or standard SymPy group types.
    """
    # H_1: G is a finitely generated group
    try:
        if hasattr(witness, 'is_finitely_generated'):
            h1_ok = bool(witness.is_finitely_generated)
        elif hasattr(witness, 'generators'):
            # If it has a generators attribute, we assume it's finitely generated
            # (SymPy groups return a finite list/tuple of generators)
            h1_ok = True
        elif isinstance(witness, PermutationGroup) or type(witness).__name__ in ['FpGroup', 'FreeGroup']:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: G is not finitely presented
    try:
        if hasattr(witness, 'is_finitely_presented'):
            neg_q_ok = not bool(witness.is_finitely_presented)
        elif isinstance(witness, PermutationGroup) or type(witness).__name__ in ['FpGroup', 'FreeGroup']:
            # All these SymPy group types are finitely presented by definition
            neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "¬Q: G is not finitely presented"
]

N_HYP = 1
NEG_Q_INDEX = 1