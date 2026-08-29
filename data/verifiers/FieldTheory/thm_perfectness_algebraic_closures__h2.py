import sympy
from sympy.abc import x, y, z, t
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # The witness could be a single field (used for both F and F_bar), 
    # a tuple (F, F_bar), or a dictionary.
    if isinstance(witness, tuple) and len(witness) == 2:
        F, F_bar = witness
    elif isinstance(witness, dict) and 'F' in witness and 'F_bar' in witness:
        F = witness['F']
        F_bar = witness['F_bar']
    else:
        F = witness
        F_bar = witness

    # H_1: Let F be a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False

    # ¬Q: The field F_bar is NOT a perfect field
    try:
        if not getattr(F_bar, 'is_Field', False):
            neg_q = False
        else:
            char = getattr(F_bar, 'char', 0)
            if char == 0:
                # Fields of characteristic 0 are always perfect
                is_perf = True
            elif type(F_bar).__name__ == 'FractionField':
                # In characteristic p > 0, a rational function field (FractionField) 
                # is not perfect because the indeterminate has no p-th root.
                is_perf = False
            else:
                # Finite fields and their algebraic extensions are perfect.
                # We assume perfectness for other types to avoid false positives.
                is_perf = True
            
            neg_q = not is_perf
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: F_bar is not a perfect field"
]

N_HYP = 1
NEG_Q_INDEX = 1