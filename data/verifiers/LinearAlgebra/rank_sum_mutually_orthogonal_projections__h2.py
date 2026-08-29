import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: witness is a list/tuple of square matrices of the same dimension
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) == 0:
            h1 = False
        else:
            h1 = True
            if not hasattr(witness[0], 'rows') or not hasattr(witness[0], 'cols'):
                h1 = False
            else:
                n = witness[0].rows
                if n != witness[0].cols:
                    h1 = False
                else:
                    for P in witness:
                        if not hasattr(P, 'rows') or not hasattr(P, 'cols'):
                            h1 = False
                            break
                        if P.rows != n or P.cols != n:
                            h1 = False
                            break
    except Exception:
        h1 = False

    # H2: P_i P_j = 0 for all i != j
    try:
        h2 = True
        if h1:
            k = len(witness)
            n = witness[0].rows
            Z = zeros(n, n)
            for i in range(k):
                for j in range(k):
                    if i != j:
                        prod = witness[i] * witness[j]
                        if prod != Z:
                            h2 = False
                            break
                if not h2:
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: rank(sum P_i) != sum(rank(P_i))
    try:
        if h1:
            k = len(witness)
            n = witness[0].rows
            sum_P = zeros(n, n)
            for P in witness:
                sum_P = sum_P + P
            
            rank_sum = sum_P.rank()
            sum_ranks = sum(P.rank() for P in witness)
            
            neg_q = bool(rank_sum != sum_ranks)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space (witness is a list of square matrices of same size)",
    "H_2: P_i P_j = 0 for all i != j",
    "¬Q: The rank of the sum of P_i is not equal to the sum of their ranks"
]

N_HYP = 2
NEG_Q_INDEX = 2