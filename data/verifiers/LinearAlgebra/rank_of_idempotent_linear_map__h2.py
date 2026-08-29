import sympy as sp
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: V is a finite-dimensional vector space over a field F of characteristic zero
    # We interpret this as the witness being a square matrix without modulo arithmetic.
    try:
        h1_ok = bool(hasattr(witness, 'is_square') and witness.is_square)
        if h1_ok:
            for elem in witness:
                if hasattr(elem, 'has') and elem.has(sp.Mod):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: T is idempotent, meaning T ∘ T = T
    try:
        diff_matrix = witness * witness - witness
        h2_ok = all(sp.simplify(elem) == 0 for elem in diff_matrix)
    except Exception:
        h2_ok = False

    # ¬Q: The rank of T is not equal to the trace of T
    try:
        diff = sp.simplify(witness.rank() - witness.trace())
        neg_q_ok = bool(diff != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F of characteristic zero",
    "H_2: T is idempotent, meaning T ∘ T = T",
    "¬Q: The rank of T is not equal to the trace of T"
]

N_HYP = 2
NEG_Q_INDEX = 2