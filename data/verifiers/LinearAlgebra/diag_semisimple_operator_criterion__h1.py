import sympy as sp
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: T is a linear operator on V
        # Represented by a square matrix
        h1 = hasattr(witness, 'is_square') and witness.is_square
    except Exception:
        h1 = False

    try:
        # H_2: For every T-invariant subspace W of V, there exists a T-invariant subspace U of V 
        # such that V is the direct sum of W and U.
        # This is the definition of a semisimple operator. Over a perfect field (like QQ), 
        # an operator is semisimple iff it is diagonalizable over the algebraic closure (C).
        h2 = h1 and witness.is_diagonalizable()
    except Exception:
        h2 = False

    try:
        # Conclusion: T is diagonalizable over F.
        # We assume F is the field of rational numbers (QQ).
        # T is diagonalizable over QQ iff it is diagonalizable over C and all its eigenvalues are in QQ.
        if not h1:
            neg_q = False
        else:
            evs = witness.eigenvals()
            is_diag_C = witness.is_diagonalizable()
            all_rational_evs = all(ev.is_rational == True for ev in evs.keys())
            q = is_diag_C and all_rational_evs
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: For every T-invariant subspace W of V, there exists a T-invariant subspace U of V such that V is the direct sum of W and U",
    "¬Q: T is not diagonalizable over F"
]

N_HYP = 2
NEG_Q_INDEX = 2