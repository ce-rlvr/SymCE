import sympy
from sympy import Matrix, zeros, simplify, eye, Tuple

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            beta = witness['beta']
            x = witness['x']
        elif isinstance(witness, (list, tuple, Tuple)) and len(witness) == 2:
            beta, x = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: V is an inner product space
    try:
        h1 = True
        if not isinstance(x, Matrix):
            h1 = False
        else:
            dim = x.shape[0]
            if x.shape[1] != 1:
                h1 = False
            if not isinstance(beta, (list, tuple, Tuple)):
                h1 = False
            else:
                for v in beta:
                    if not isinstance(v, Matrix) or v.shape != (dim, 1):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: W is a finite-dimensional subspace of V
    try:
        h2 = isinstance(beta, (list, tuple, Tuple))
    except Exception:
        h2 = False

    # H3: beta is an orthonormal basis for W
    try:
        h3 = True
        if h1 and h2:
            for i in range(len(beta)):
                for j in range(len(beta)):
                    dot_prod = (beta[i].H * beta[j])[0, 0]
                    if i == j:
                        if simplify(dot_prod - 1) != 0:
                            h3 = False
                    else:
                        if simplify(dot_prod) != 0:
                            h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: x != sum(<x, v_i> v_i)
    try:
        neg_q = False
        if h1 and h2:
            projection = zeros(dim, 1)
            for v in beta:
                coef = (v.H * x)[0, 0]
                projection += coef * v
            
            diff = x - projection
            is_zero = True
            for i in range(dim):
                if simplify(diff[i, 0]) != 0:
                    is_zero = False
                    break
            neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: W is a finite-dimensional subspace of V",
    "H_3: beta is an orthonormal basis for W",
    "¬Q: x != sum(<x, v_i> v_i)"
]

N_HYP = 3
NEG_Q_INDEX = 3