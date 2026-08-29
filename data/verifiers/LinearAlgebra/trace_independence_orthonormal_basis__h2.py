import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            E = witness.get("E")
            F = witness.get("F")
            T = witness.get("T")
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            E, F, T = witness[0], witness[1], witness[2]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: V is a finite-dimensional inner product space
    try:
        h1 = False
        if isinstance(E, (list, tuple)) and isinstance(F, (list, tuple)):
            if len(E) > 0 and len(E) == len(F):
                n = E[0].shape[0]
                if all(isinstance(v, Matrix) and v.shape == (n, 1) for v in list(E) + list(F)):
                    h1 = True
    except Exception:
        h1 = False

    # H2: {e_1, ..., e_n} is an orthonormal basis of V
    try:
        h2 = False
        if h1:
            n = len(E)
            is_orthonormal = True
            for i in range(n):
                for j in range(n):
                    dot_prod = (E[i].H * E[j])[0, 0]
                    expected = 1 if i == j else 0
                    diff = sympy.simplify(sympy.expand(dot_prod - expected))
                    if diff != 0:
                        is_orthonormal = False
                        break
                if not is_orthonormal:
                    break
            h2 = is_orthonormal
    except Exception:
        h2 = False

    # H3: {f_1, ..., f_n} is an orthonormal basis of V
    try:
        h3 = False
        if h1:
            n = len(F)
            is_orthonormal = True
            for i in range(n):
                for j in range(n):
                    dot_prod = (F[i].H * F[j])[0, 0]
                    expected = 1 if i == j else 0
                    diff = sympy.simplify(sympy.expand(dot_prod - expected))
                    if diff != 0:
                        is_orthonormal = False
                        break
                if not is_orthonormal:
                    break
            h3 = is_orthonormal
    except Exception:
        h3 = False

    # neg_Q: \sum <T e_i, e_i> != \sum <T f_i, f_i>
    try:
        neg_q = False
        if h1:
            n = len(E)
            sum_E = 0
            for i in range(n):
                Te = T(E[i])
                if not isinstance(Te, Matrix) or Te.shape != (n, 1):
                    raise ValueError("T must return a column vector of the same dimension")
                sum_E += (E[i].H * Te)[0, 0]
            
            sum_F = 0
            for i in range(n):
                Tf = T(F[i])
                if not isinstance(Tf, Matrix) or Tf.shape != (n, 1):
                    raise ValueError("T must return a column vector of the same dimension")
                sum_F += (F[i].H * Tf)[0, 0]
            
            diff = sympy.simplify(sympy.expand(sum_E - sum_F))
            if diff != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: {e_1, ..., e_n} is an orthonormal basis of V",
    "H_3: {f_1, ..., f_n} is an orthonormal basis of V",
    "¬Q: \\sum_{i=1}^n \\langle T e_i, e_i \\rangle \\neq \\sum_{i=1}^n \\langle T f_i, f_i \\rangle"
]

N_HYP = 3
NEG_Q_INDEX = 3