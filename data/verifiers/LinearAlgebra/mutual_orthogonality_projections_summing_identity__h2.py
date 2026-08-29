import sympy
from sympy import Matrix, eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if isinstance(witness, (list, tuple)) and len(witness) >= 1:
            n = witness[0].shape[0]
            is_valid = True
            for P in witness:
                if not getattr(P, "is_Matrix", False):
                    is_valid = False
                    break
                if P.shape != (n, n):
                    is_valid = False
                    break
                if P * P != P:
                    is_valid = False
                    break
            h1 = is_valid
    except Exception:
        h1 = False

    try:
        neg_q = False
        if isinstance(witness, (list, tuple)) and len(witness) >= 2:
            n = witness[0].shape[0]
            for i in range(len(witness)):
                for j in range(len(witness)):
                    if i != j:
                        if witness[i] * witness[j] != zeros(n, n):
                            neg_q = True
                            break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P_1, P_2, ..., P_k are n x n projection matrices (P_i^2 = P_i)",
    "¬Q: The matrices are not mutually orthogonal (there exist i != j such that P_i P_j != 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1