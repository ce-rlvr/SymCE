import sympy as sp
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a real inner product space",
    "H_2: G is the n x n Gram matrix defined by G_{ij} = <v_i, v_j>",
    "¬Q: The Gram matrix G is not orthogonally diagonalizable over the real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Handle tuple witness (e.g., (V, G))
        if isinstance(witness, tuple) and len(witness) == 2:
            _, G = witness
            witness = G

        # Handle list of vectors witness
        if isinstance(witness, list) and all(isinstance(v, Matrix) for v in witness):
            n = len(witness)
            G = sp.zeros(n, n)
            for i in range(n):
                for j in range(n):
                    G[i, j] = witness[i].dot(witness[j])
            witness = G

        if not isinstance(witness, Matrix):
            return [False, False, False]

        # H1: V is a real inner product space
        # We verify this by checking that the resulting Gram matrix has real, finite entries.
        h1 = True
        for val in witness:
            if val.is_real is False or val.is_finite is False:
                h1 = False
                break
            if val.is_real is None:
                try:
                    val_num = val.evalf()
                    if val_num.is_real is False or val_num.is_finite is False:
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break

        # H2: G is the n x n Gram matrix
        # A matrix is a Gram matrix of real vectors iff it is symmetric and positive semi-definite.
        h2 = False
        if witness.is_square and witness.is_symmetric():
            h2 = True
            psd = getattr(witness, 'is_positive_semidefinite', None)
            if psd is False:
                h2 = False
            elif psd is None:
                try:
                    for ev in witness.eigenvals():
                        ev_num = ev.evalf()
                        if ev_num.is_real and ev_num < 0:
                            h2 = False
                            break
                except Exception:
                    h2 = False

        # ¬Q: The Gram matrix G is NOT orthogonally diagonalizable over the real numbers.
        # By the Spectral Theorem, a real matrix is orthogonally diagonalizable iff it is symmetric.
        neg_q = not witness.is_symmetric()

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]