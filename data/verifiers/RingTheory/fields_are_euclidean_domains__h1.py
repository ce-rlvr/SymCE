import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ
R = RR
C = CC

def conditions(witness):
    # Map sympy.S sets to polys domains if provided
    if witness is sympy.S.Integers:
        witness = ZZ
    elif witness is sympy.S.Rationals:
        witness = QQ
    elif witness is sympy.S.Reals:
        witness = RR
    elif witness is sympy.S.Complexes:
        witness = CC

    try:
        # H_1: Let d: F \ {0} -> N be the constant function d(x) = 1.
        # This is a definitional setup that is valid for any ring with a zero element.
        # We verify the witness is a valid ring/domain structure in SymPy.
        h1 = hasattr(witness, 'zero') and hasattr(witness, 'is_Field')
    except Exception:
        h1 = False

    try:
        # ¬Q: F is not a Euclidean domain with respect to the Euclidean function d.
        # For d(x) = 1, the condition d(r) < d(b) is impossible since d maps to N and d(x)=1.
        # Thus, the division algorithm a = bq + r requires r = 0 for all a, b (b != 0).
        # This implies every non-zero element divides every element, which means F must be a field.
        # Therefore, F is a Euclidean domain w.r.t d(x)=1 if and only if F is a field.
        # The conclusion fails (¬Q is True) iff F is NOT a field.
        neg_q = not bool(witness.is_Field)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let d: F \\ {0} -> N be the constant function d(x) = 1",
    "¬Q: F is not a Euclidean domain with respect to d"
]

N_HYP = 1
NEG_Q_INDEX = 1