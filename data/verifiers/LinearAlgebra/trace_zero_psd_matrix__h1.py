import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is symmetric",
    "H_2: A is positive semidefinite",
    "H_3: The trace of A is equal to zero",
    "¬Q: A is not the zero matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # H1: A is symmetric
    try:
        if hasattr(witness, 'is_symmetric'):
            h1 = bool(witness.is_symmetric())
        else:
            h1 = bool(witness == witness.transpose())
    except Exception:
        h1 = False

    # H2: A is positive semidefinite
    try:
        h2 = False
        # First, try SymPy's built-in property (strict check, usually requires Hermitian)
        if getattr(witness, 'is_positive_semidefinite', None) is True:
            h2 = True
        else:
            # Fallback: check if all eigenvalues are non-negative reals.
            # This handles complex symmetric matrices that are PSD in the eigenvalue sense.
            evs = witness.eigenvals()
            all_psd = True
            for ev in evs.keys():
                if not ev.is_real:
                    all_psd = False
                    break
                if bool(ev < 0):
                    all_psd = False
                    break
            if all_psd:
                h2 = True
    except Exception:
        h2 = False

    # H3: The trace of A is equal to zero
    try:
        tr = witness.trace()
        if hasattr(tr, 'is_zero') and tr.is_zero is not None:
            h3 = bool(tr.is_zero)
        else:
            h3 = bool(tr == 0)
    except Exception:
        h3 = False

    # neg_Q: A is not the zero matrix
    try:
        if hasattr(witness, 'is_zero_matrix') and witness.is_zero_matrix is not None:
            neg_q = not witness.is_zero_matrix
        else:
            neg_q = not all(e == 0 for e in witness)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]