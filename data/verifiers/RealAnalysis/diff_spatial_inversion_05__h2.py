import sympy as sp

# Top-level setup
x1, x2, x3, x4, x5 = sp.symbols('x1 x2 x3 x4 x5', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be:
      - A callable f(x) where x is a sympy Matrix of size n x 1.
      - A sympy Matrix representing f(x) in terms of x1, x2, ...
      - A tuple (n, f) where n is the dimension and f is a callable or sympy Matrix.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, f = witness
            if not (isinstance(n, int) and 1 <= n <= 5):
                return [False, False]
            x_vec = sp.Matrix([x1, x2, x3, x4, x5][:n])
            if callable(f):
                f_expr = f(x_vec)
            else:
                f_expr = f
            if not isinstance(f_expr, sp.Matrix):
                if isinstance(f_expr, (list, tuple)):
                    f_expr = sp.Matrix(f_expr)
                else:
                    f_expr = sp.Matrix([f_expr])
        elif isinstance(witness, sp.Matrix):
            f_expr = witness
            n = f_expr.shape[0]
            if not (1 <= n <= 5):
                return [False, False]
            x_vec = sp.Matrix([x1, x2, x3, x4, x5][:n])
        elif callable(witness):
            success = False
            for test_n in range(1, 6):
                try:
                    x_vec = sp.Matrix([x1, x2, x3, x4, x5][:test_n])
                    f_expr = witness(x_vec)
                    if not isinstance(f_expr, sp.Matrix):
                        if isinstance(f_expr, (list, tuple)):
                            f_expr = sp.Matrix(f_expr)
                        else:
                            f_expr = sp.Matrix([f_expr])
                    n = f_expr.shape[0]
                    if n == test_n:
                        success = True
                        break
                except Exception:
                    continue
            if not success:
                return [False, False]
        else:
            return [False, False]
            
        h1 = (1 <= n <= 5)
    except Exception:
        return [False, False]

    try:
        norm_x_sq = sum(x**2 for x in x_vec)
        I = sp.eye(n)
        J_expected = (1 / norm_x_sq) * I - (2 / norm_x_sq**2) * (x_vec * x_vec.T)
        
        J_actual = f_expr.jacobian(x_vec)
        
        # Evaluate at a specific point to quickly catch inequalities
        subs_dict = {x_vec[i]: sp.Rational(i + 1, 1) for i in range(n)}
        J_exp_val = J_expected.subs(subs_dict)
        J_act_val = J_actual.subs(subs_dict)
        
        diff_val = J_act_val - J_exp_val
        is_val_equal = all(sp.simplify(diff_val[i, j]) == 0 for i in range(n) for j in range(n))
        
        if not is_val_equal:
            neg_q = True
        else:
            # Full symbolic check if numerical evaluation matches
            diff = J_actual - J_expected
            is_equal = all(sp.simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
            neg_q = not is_equal
    except Exception:
        # If jacobian computation or simplification fails, it's not differentiable as required
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U = \\mathbb{R}^n \\setminus \\{0\\}",
    "¬Q: f is not differentiable on U, or its Jacobian is not the spatial inversion Jacobian"
]

N_HYP = 1
NEG_Q_INDEX = 1