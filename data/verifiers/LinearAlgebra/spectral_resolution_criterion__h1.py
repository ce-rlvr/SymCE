import sympy
from sympy import eye, zeros, Matrix

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: There exist k distinct scalars lambda_i in F",
    "H_2: There exist k non-zero matrices E_i over F such that E_i^2 = E_i and E_i E_j = 0 for i != j",
    "H_3: The sum of the matrices E_i equals the n x n identity matrix I",
    "H_4: A can be expressed as the linear combination A = sum lambda_i E_i",
    "¬Q: The matrix A is not diagonalizable over the field F"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness['A']
            lambdas = witness['lambdas']
            Es = witness['Es']
        elif isinstance(witness, tuple) and len(witness) == 3:
            A, lambdas, Es = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        if A.shape[0] != A.shape[1]:
            return [False] * 5
        n = A.shape[0]
    except Exception:
        return [False] * 5

    # H_1: k distinct scalars
    try:
        k = len(Es)
        if len(lambdas) != k:
            h1 = False
        else:
            h1 = True
            for i in range(k):
                for j in range(i + 1, k):
                    diff = lambdas[i] - lambdas[j]
                    if hasattr(diff, 'expand'):
                        diff = diff.expand()
                    if diff == 0:
                        h1 = False
    except Exception:
        h1 = False

    # H_2: k non-zero matrices, E_i^2 = E_i, E_i E_j = 0
    try:
        h2 = True
        for i in range(k):
            if Es[i].expand().is_zero_matrix == True:
                h2 = False
                break
            diff = Es[i] * Es[i] - Es[i]
            if diff.expand().is_zero_matrix != True:
                h2 = False
                break
            for j in range(k):
                if i != j:
                    prod = Es[i] * Es[j]
                    if prod.expand().is_zero_matrix != True:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H_3: sum E_i = I
    try:
        if k == 0:
            h3 = (n == 0)
        else:
            I = eye(n)
            sum_E = sum(Es[1:], Es[0])
            diff = sum_E - I
            h3 = (diff.expand().is_zero_matrix == True)
    except Exception:
        h3 = False

    # H_4: A = sum lambda_i E_i
    try:
        if k == 0:
            h4 = (A.expand().is_zero_matrix == True)
        else:
            sum_lam_E = sum([lambdas[i] * Es[i] for i in range(k)], Es[0]*0)
            diff = A - sum_lam_E
            h4 = (diff.expand().is_zero_matrix == True)
    except Exception:
        h4 = False

    # ¬Q: A is not diagonalizable
    try:
        is_diag = A.is_diagonalizable()
        if is_diag is True:
            neg_q = False
        elif is_diag is False:
            neg_q = True
        else:
            P, D = A.diagonalize()
            neg_q = False
    except Exception:
        try:
            eigenvals = A.eigenvals()
            total_geom_mult = sum(len((A - val * eye(n)).nullspace()) for val in eigenvals)
            neg_q = not (total_geom_mult == n)
        except Exception:
            neg_q = False

    return [h1, h2, h3, h4, neg_q]