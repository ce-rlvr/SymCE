import sympy
from sympy.abc import x, y

def is_non_constant_polynomial(f, x, y):
    try:
        if not isinstance(f, sympy.Expr):
            return False
        # The polynomial must only depend on x and y (or be constant)
        if not f.free_symbols.issubset({x, y}):
            return False
        if not f.is_polynomial(x, y):
            return False
        poly = sympy.poly(f, x, y)
        return not poly.is_constant()
    except Exception:
        return False

def has_infinitely_many_real_solutions(f, x, y):
    try:
        if not isinstance(f, sympy.Expr):
            return False
            
        try:
            poly = sympy.poly(f, x, y)
            # If the polynomial has non-real coefficients, it's over a field like C.
            # Over an algebraically closed field, any non-constant bivariate polynomial
            # has infinitely many zeros. Thus the conclusion holds (not a counterexample).
            if not all(c.is_real for c in poly.coeffs()):
                return True
        except Exception:
            pass

        # 1. Grid check for sign change
        # If a polynomial changes sign on R^2, it has infinitely many real zeros.
        pos = False
        neg = False
        grid = [i * 1.0 for i in range(-10, 11)]
        for i in grid:
            for j in grid:
                try:
                    val = complex(f.subs({x: i, y: j}))
                    if abs(val.imag) < 1e-9:
                        if val.real > 1e-9:
                            pos = True
                        elif val.real < -1e-9:
                            neg = True
                    if pos and neg:
                        return True
                except Exception:
                    pass

        # Generate a diverse set of test points to evaluate branches
        test_points = set()
        for scale in [10, 1, 0.1, 0.01, 0.001, 0.0001]:
            for i in range(-50, 51):
                test_points.add(i * 0.1234 * scale)
        test_points = list(test_points)
            
        # 2. Try solving for y in terms of x
        try:
            branches = sympy.solve(f, y)
            for b in branches:
                real_count = 0
                try:
                    b_lam = sympy.lambdify(x, b, modules=['math', 'cmath'])
                    for tp in test_points:
                        try:
                            val = complex(b_lam(tp))
                            if abs(val.imag) < 1e-9:
                                real_count += 1
                                if real_count > 10:
                                    return True
                        except Exception:
                            pass
                except Exception:
                    # Fallback to subs if lambdify fails
                    for tp in test_points:
                        try:
                            val = complex(b.subs(x, tp))
                            if abs(val.imag) < 1e-9:
                                real_count += 1
                                if real_count > 10:
                                    return True
                        except Exception:
                            pass
        except Exception:
            pass

        # 3. Try solving for x in terms of y
        try:
            branches = sympy.solve(f, x)
            for b in branches:
                real_count = 0
                try:
                    b_lam = sympy.lambdify(y, b, modules=['math', 'cmath'])
                    for tp in test_points:
                        try:
                            val = complex(b_lam(tp))
                            if abs(val.imag) < 1e-9:
                                real_count += 1
                                if real_count > 10:
                                    return True
                        except Exception:
                            pass
                except Exception:
                    for tp in test_points:
                        try:
                            val = complex(b.subs(y, tp))
                            if abs(val.imag) < 1e-9:
                                real_count += 1
                                if real_count > 10:
                                    return True
                        except Exception:
                            pass
        except Exception:
            pass

        # If no sign change and branches yield few/no real points, it has finitely many real solutions.
        return False
    except Exception:
        return False

def conditions(witness):
    h1_ok = is_non_constant_polynomial(witness, x, y)
    
    try:
        inf_sols = has_infinitely_many_real_solutions(witness, x, y)
        neg_q_ok = not inf_sols
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x, y) is a non-constant polynomial",
    "¬Q: f(x, y) = 0 has finitely many distinct solutions"
]

N_HYP = 1
NEG_Q_INDEX = 1