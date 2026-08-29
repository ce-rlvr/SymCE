import sympy as sp
from sympy import Matrix, eye, zeros, Symbol

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
t_sym = Symbol('t')
lam_sym = Symbol('lambda')

def is_zero(expr):
    if expr == 0:
        return True
    try:
        if sp.simplify(expr) == 0:
            return True
        if sp.expand(expr) == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if isinstance(witness, dict):
            J = witness.get('J')
            t = witness.get('t')
            lam = witness.get('lam', witness.get('lambda_', None))
            if lam is None and J is not None:
                try:
                    lam = J[0, 0]
                except Exception:
                    pass
        else:
            if len(witness) == 3:
                J, t, lam = witness
            elif len(witness) == 2:
                J, t = witness
                lam = J[0, 0]
            else:
                return [False, False]
    except Exception:
        return [False, False]

    # H_1: t is a scalar
    try:
        if isinstance(t, (int, float, complex, sp.Expr)) and not getattr(t, 'is_Matrix', False):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The matrix exponential e^{Jt} is NOT an upper triangular matrix where 
    # the (i, j)-th entry for j >= i is given by (t^{j-i} / (j-i)!) e^{lambda t}.
    try:
        J = Matrix(J)
        if J.rows != J.cols or J.rows == 0:
            neg_q = False
        else:
            E = (J * t).exp()
            is_correct_form = True
            for i in range(J.rows):
                for j in range(J.cols):
                    if j < i:
                        if not is_zero(E[i, j]):
                            is_correct_form = False
                            break
                    else:
                        expected = (t**(j - i) / sp.factorial(j - i)) * sp.exp(lam * t)
                        if not is_zero(E[i, j] - expected):
                            is_correct_form = False
                            break
                if not is_correct_form:
                    break
            neg_q = not is_correct_form
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: t is a scalar",
    "¬Q: e^{Jt} does not match the Jordan block exponential formula"
]

N_HYP = 1
NEG_Q_INDEX = 1