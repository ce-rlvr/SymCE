import sympy
from sympy.matrices import MatrixBase

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            sigma_n = witness.get('sigma_n')
            sigma_1 = witness.get('sigma_1')
        elif hasattr(witness, 'A') and hasattr(witness, 'sigma_n') and hasattr(witness, 'sigma_1'):
            A = witness.A
            sigma_n = witness.sigma_n
            sigma_1 = witness.sigma_1
        else:
            A, sigma_n, sigma_1 = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an invertible n x n complex matrix
    try:
        h1 = isinstance(A, MatrixBase) and A.is_square and (A.det() != 0)
    except Exception:
        h1 = False

    # H_2: sigma_n is the smallest singular value of A
    try:
        svs = A.singular_values()
        smallest_sv = svs[-1]
        h2 = (sigma_n == smallest_sv) or (sympy.simplify(sigma_n - smallest_sv) == 0)
        if not h2:
            try:
                h2 = abs(complex(sigma_n) - complex(smallest_sv)) < 1e-9
            except Exception:
                pass
    except Exception:
        h2 = False

    # neg_Q: kappa_2(A) != sigma_1 / sigma_n
    try:
        svs = A.singular_values()
        kappa = svs[0] / svs[-1]
        rhs = sigma_1 / sigma_n
        
        is_eq = (kappa == rhs) or (sympy.simplify(kappa - rhs) == 0)
        if not is_eq:
            try:
                is_eq = abs(complex(kappa) - complex(rhs)) < 1e-9
            except Exception:
                pass
        neg_q = not is_eq
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an invertible n x n complex matrix",
    "H_2: sigma_n is the smallest singular value of A",
    "¬Q: kappa_2(A) != sigma_1 / sigma_n"
]

N_HYP = 2
NEG_Q_INDEX = 2