import sympy
from sympy import symbols

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t = symbols('x y z t')
x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

def conditions(witness) -> list[bool]:
    try:
        # Parse witness: can be a sympy expression or a tuple (expr, vars)
        if isinstance(witness, tuple):
            expr, vars = witness
            vars = list(vars)
        else:
            expr = witness
            vars = list(expr.free_symbols)
            if not vars:
                vars = [x]
                
        # H1: U is an open neighborhood of the origin in R^n
        # We check if the function can be evaluated at the origin and returns a real finite value.
        try:
            val_at_0 = expr.subs({v: 0 for v in vars})
            h1 = not val_at_0.has(sympy.oo, sympy.zoo, sympy.nan) and getattr(val_at_0, 'is_real', None) is not False
        except Exception:
            h1 = False
            
        # H2: f is a three times continuously differentiable function
        # We check if all 3rd order partial derivatives exist and are finite at the origin.
        try:
            h2 = True
            for v1 in vars:
                for v2 in vars:
                    for v3 in vars:
                        d3 = sympy.diff(expr, v1, v2, v3)
                        d3_val = d3.subs({v: 0 for v in vars})
                        if getattr(d3_val, 'is_real', None) is False or d3_val.has(sympy.oo, sympy.zoo, sympy.nan):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
        except Exception:
            h2 = False
            
        # H3: f(0) = 0
        try:
            h3 = bool(sympy.simplify(val_at_0) == 0)
        except Exception:
            h3 = False
            
        # H4: The gradient \nabla f(0) is the zero vector
        try:
            h4 = True
            for v in vars:
                d1 = sympy.diff(expr, v)
                d1_val = d1.subs({v: 0 for v in vars})
                if not sympy.simplify(d1_val) == 0:
                    h4 = False
                    break
        except Exception:
            h4 = False
            
        # ¬Q: The conclusion fails
        # The conclusion asserts the existence of a local diffeomorphism transforming f into a non-degenerate quadratic form.
        # This is only possible if the Hessian of f at 0 is non-degenerate.
        # Thus, the conclusion fails if and only if the Hessian at 0 is degenerate (determinant is 0).
        try:
            hessian_matrix = sympy.zeros(len(vars), len(vars))
            for i, v1 in enumerate(vars):
                for j, v2 in enumerate(vars):
                    d2 = sympy.diff(expr, v1, v2)
                    d2_val = d2.subs({v: 0 for v in vars})
                    hessian_matrix[i, j] = d2_val
            det_hessian = hessian_matrix.det()
            neg_q = bool(sympy.simplify(det_hessian) == 0)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: U is an open neighborhood of the origin in R^n",
    "H_2: f is a three times continuously differentiable function",
    "H_3: f(0) = 0",
    "H_4: The gradient \\nabla f(0) is the zero vector",
    "¬Q: The conclusion fails (Hessian at 0 is degenerate, so no such diffeomorphism exists)"
]

N_HYP = 4
NEG_Q_INDEX = 4