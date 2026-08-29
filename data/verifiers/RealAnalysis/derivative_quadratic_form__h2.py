import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            a = witness.get('a')
            f = witness.get('f')
            x = witness.get('x', None)
        else:
            if len(witness) == 3:
                A, a, f = witness
                x = None
            elif len(witness) == 4:
                A, a, f, x = witness
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: A is an n x n real matrix
    try:
        A_mat = sp.Matrix(A)
        h1 = A_mat.is_square and all(e.is_real is not False for e in A_mat)
    except Exception:
        h1 = False

    # H_2: a is in R^n
    try:
        a_mat = sp.Matrix(a)
        n = A_mat.shape[0] if 'A_mat' in locals() else (len(x) if x else a_mat.shape[0])
        h2 = a_mat.shape == (n, 1) and all(e.is_real is not False for e in a_mat)
    except Exception:
        h2 = False

    # ¬Q: f is not infinitely differentiable at a, or its gradient is not (A + A^T)a
    try:
        if not h1 or not h2:
            n_dim = A_mat.shape[0] if 'A_mat' in locals() else 1
        else:
            n_dim = A_mat.shape[0]

        if callable(f):
            if x is None:
                x = sp.symbols(f'x0:{n_dim}')
            f_expr = f(*x)
        else:
            f_expr = f
            if x is None:
                if hasattr(f_expr, 'free_symbols'):
                    x = sorted(list(f_expr.free_symbols), key=lambda s: s.name)
                else:
                    x = []
                if len(x) < n_dim:
                    dummy = sp.symbols(f'dummy0:{n_dim}')
                    x = x + [d for d in dummy if d not in x][:n_dim - len(x)]
                elif len(x) > n_dim:
                    x = x[:n_dim]

        if len(x) != n_dim:
            neg_q = True
        else:
            grad_f = sp.Matrix([sp.diff(f_expr, xi) for xi in x])
            subs_dict = {x[i]: a_mat[i, 0] for i in range(n_dim)}
            grad_f_a = grad_f.subs(subs_dict)
            
            expected_grad = (A_mat + A_mat.T) * a_mat
            
            is_eq = True
            for i in range(n_dim):
                diff_val = sp.simplify(grad_f_a[i, 0] - expected_grad[i, 0])
                if diff_val != 0:
                    is_eq = False
                    break
            neg_q = not is_eq
    except Exception:
        # If differentiation, substitution, or matrix operations fail, 
        # the function does not satisfy the conclusion.
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n real matrix",
    "H_2: a is in R^n",
    "¬Q: f is not infinitely differentiable at a, or its gradient is not (A + A^T)a"
]

N_HYP = 2
NEG_Q_INDEX = 2