import sympy
from sympy import Matrix, eye, zeros, im, re, simplify
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) < 2:
            return [False, False, False]
        A = witness[0]
        k = witness[1]
        if not hasattr(A, 'eigenvals') or not hasattr(A, 'shape'):
            return [False, False, False]
        if A.shape[0] != A.shape[1]:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: The eigenvalues of A are ordered as lambda_1 <= ... <= lambda_n
    # This implies that all eigenvalues of A must be real numbers.
    try:
        evs = A.eigenvals(multiple=True)
        h1 = True
        for ev in evs:
            if ev.is_real is False:
                h1 = False
                break
            elif ev.is_real is None:
                try:
                    if abs(complex(ev).imag) > 1e-9:
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: k is an integer such that 1 <= k <= n
    try:
        n = A.shape[0]
        h2 = (int(k) == k) and (1 <= k <= n)
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails.
    # The conclusion states the min-max formula holds for the k-th eigenvalue.
    # The formula uses the complex inner product (x^* A x). If A is not Hermitian,
    # the Rayleigh quotient can take non-real values, making the maximum undefined.
    # Thus, the equality fails if A is not Hermitian.
    try:
        diff = A - A.H
        is_hermitian = False
        if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
            is_hermitian = True
        else:
            try:
                is_hermitian = all(abs(complex(diff[i, j])) < 1e-9 for i in range(A.shape[0]) for j in range(A.shape[1]))
            except Exception:
                try:
                    is_hermitian = simplify(diff).is_zero_matrix
                except Exception:
                    pass
        neg_q = not is_hermitian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The eigenvalues of A are ordered as lambda_1 <= ... <= lambda_n (i.e., they are real)",
    "H_2: k is an integer such that 1 <= k <= n",
    "¬Q: The k-th eigenvalue is NOT given by the min-max formula (e.g., max is undefined because A is not Hermitian)"
]

N_HYP = 2
NEG_Q_INDEX = 2