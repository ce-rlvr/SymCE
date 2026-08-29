import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be a matrix whose rows/columns span a subspace W of V = F^n),
    check if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: V is a vector space over a field F
    # Any valid matrix implicitly defines a subspace W of the vector space V = F^n.
    try:
        W = Matrix(witness)
        h1_ok = hasattr(W, 'shape') and len(W.shape) == 2
    except Exception:
        h1_ok = False

    # ¬Q: The annihilator W^0 is not equal to V^*
    # W^0 = V^* if and only if W is the zero subspace.
    # Therefore, W^0 != V^* if and only if W is NOT the zero subspace.
    try:
        W = Matrix(witness)
        neg_q_ok = not W.is_zero_matrix
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: The annihilator W^0 is not equal to V^* (i.e., W is not the zero subspace)"
]

N_HYP = 1
NEG_Q_INDEX = 1