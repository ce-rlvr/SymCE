import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                A, lambdas, sigmas, k = witness
            elif len(witness) == 3:
                A, lambdas, k = witness
                sigmas = None
            elif len(witness) == 2:
                A, k = witness
                lambdas = None
                sigmas = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: A is an n x n complex matrix
    try:
        if not isinstance(A, sp.Matrix):
            h1 = False
        elif A.rows != A.cols:
            h1 = False
        else:
            h1 = True
            n = A.rows
    except Exception:
        h1 = False

    # H2: lambda_1, ..., lambda_n are the eigenvalues of A sorted by absolute value descending
    try:
        if not h1:
            h2 = False
        elif lambdas is None:
            evals = A.eigenvals()
            lambdas = []
            for val, mult in evals.items():
                lambdas.extend([val] * mult)
            lambdas.sort(key=lambda x: float(sp.Abs(x).evalf()), reverse=True)
            h2 = True
        else:
            if len(lambdas) != n:
                h2 = False
            else:
                sorted_correctly = True
                for i in range(len(lambdas) - 1):
                    if float(sp.Abs(lambdas[i]).evalf()) < float(sp.Abs(lambdas[i+1]).evalf()) - 1e-9:
                        sorted_correctly = False
                        break
                
                evals = A.eigenvals()
                expected_lambdas = []
                for val, mult in evals.items():
                    expected_lambdas.extend([val] * mult)
                
                def canonical_key(x):
                    try:
                        c = complex(sp.N(x))
                        return (round(c.real, 5), round(c.imag, 5))
                    except Exception:
                        return (0, 0)
                
                l1 = sorted(lambdas, key=canonical_key)
                l2 = sorted(expected_lambdas, key=canonical_key)
                
                matches = True
                for x, y in zip(l1, l2):
                    if abs(complex(sp.N(x)) - complex(sp.N(y))) > 1e-5:
                        matches = False
                        break
                h2 = sorted_correctly and matches
    except Exception:
        h2 = False

    # H3: k is an integer such that 1 <= k <= n
    try:
        if not h1:
            h3 = False
        else:
            k_val = int(k)
            if k_val != float(k):
                h3 = False
            else:
                h3 = (1 <= k_val <= n)
    except Exception:
        h3 = False

    # neg_Q: The product of the first k absolute eigenvalues is strictly greater than the product of the first k singular values
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            expected_sigmas = A.singular_values()
            if sigmas is None:
                sigmas_to_use = expected_sigmas
            else:
                s1 = sorted([float(sp.N(x)) for x in sigmas])
                s2 = sorted([float(sp.N(x)) for x in expected_sigmas])
                matches = True
                if len(s1) != len(s2):
                    matches = False
                else:
                    for x, y in zip(s1, s2):
                        if abs(x - y) > 1e-5:
                            matches = False
                            break
                if matches:
                    sigmas_to_use = sigmas
                else:
                    sigmas_to_use = expected_sigmas

            prod_lambdas = 1.0
            for i in range(k_val):
                prod_lambdas *= float(sp.Abs(lambdas[i]).evalf())
                
            prod_sigmas = 1.0
            for i in range(k_val):
                prod_sigmas *= float(sp.N(sigmas_to_use[i]))
                
            neg_q = prod_lambdas > prod_sigmas + 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "H_2: lambda_1, ..., lambda_n are the eigenvalues of A sorted by absolute value descending",
    "H_3: k is an integer such that 1 <= k <= n",
    "¬Q: The product of the first k absolute eigenvalues is strictly greater than the product of the first k singular values"
]

N_HYP = 3
NEG_Q_INDEX = 3