import sympy as sp
from sympy import eye, zeros
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
            f_expr = witness.get('f')
            vars = witness.get('vars')
            a = witness.get('a')
            U = witness.get('U', None)
        else:
            f_expr = getattr(witness, 'f', None)
            vars = getattr(witness, 'vars', None)
            a = getattr(witness, 'a', None)
            U = getattr(witness, 'U', None)
            
        if f_expr is None or vars is None or a is None:
            return [False, False, False, False, False]
            
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
            
        if not isinstance(a, (list, tuple)):
            a = [a]
            
        if not isinstance(f_expr, sp.Matrix):
            if isinstance(f_expr, (list, tuple)):
                f_expr = sp.Matrix(f_expr)
            else:
                f_expr = sp.Matrix([f_expr])
                
        n = len(vars)
    except Exception:
        return [False, False, False, False, False]

    # H1: U is an open subset of R^n
    h1 = False
    try:
        if U is None:
            h1 = True
        elif hasattr(U, 'is_open'):
            h1 = U.is_open is not False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: f is continuous and injective on U
    h2 = False
    try:
        is_injective = True
        if n == 1:
            x = vars[0]
            pts = [-10, -5, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 5, 10]
            vals = {}
            for p in pts:
                try:
                    v = float(sp.re(f_expr[0].subs(x, p).evalf()))
                    for existing_v in vals:
                        if abs(v - existing_v) < 1e-7:
                            is_injective = False
                            break
                    if not is_injective:
                        break
                    vals[v] = p
                except Exception:
                    pass
            
            if is_injective:
                df = sp.diff(f_expr[0], x)
                signs = set()
                for p in pts:
                    try:
                        v = float(sp.re(df.subs(x, p).evalf()))
                        if v > 1e-7:
                            signs.add(1)
                        elif v < -1e-7:
                            signs.add(-1)
                    except Exception:
                        pass
                if len(signs) > 1:
                    is_injective = False
        else:
            pts = [-2, -1, 0, 1, 2]
            grid = list(itertools.product(pts, repeat=n))
            vals = []
            for p in grid:
                try:
                    v = tuple(float(sp.re(expr.subs(zip(vars, p)).evalf())) for expr in f_expr)
                    vals.append(v)
                except Exception:
                    pass
            for i in range(len(vals)):
                for j in range(i+1, len(vals)):
                    dist = sum((vals[i][k] - vals[j][k])**2 for k in range(n))
                    if dist < 1e-9:
                        is_injective = False
                        break
                if not is_injective:
                    break
        h2 = is_injective
    except Exception:
        h2 = False

    # H3: f is differentiable at a
    h3 = False
    try:
        J = f_expr.jacobian(vars)
        J_a = J.subs(zip(vars, a))
        if not J_a.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
            is_diff = True
            eps = 1e-6
            dirs = list(itertools.product([-1, 0, 1], repeat=n))
            dirs.remove(tuple([0]*n))
            for d in dirs:
                norm = sum(x**2 for x in d)**0.5
                d_norm = [x/norm * eps for x in d]
                pt = [float(sp.re(sp.sympify(a[i]).evalf())) + d_norm[i] for i in range(n)]
                
                f_pt = [float(sp.re(expr.subs(zip(vars, pt)).evalf())) for expr in f_expr]
                f_a = [float(sp.re(expr.subs(zip(vars, a)).evalf())) for expr in f_expr]
                
                diff = [pt[i] - float(sp.re(sp.sympify(a[i]).evalf())) for i in range(n)]
                J_diff = []
                for i in range(n):
                    row_sum = 0
                    for j in range(n):
                        row_sum += float(sp.re(J_a[i, j].evalf())) * diff[j]
                    J_diff.append(row_sum)
                
                err = sum((f_pt[i] - f_a[i] - J_diff[i])**2 for i in range(n))**0.5
                if err / eps > 1e-3:
                    is_diff = False
                    break
            h3 = is_diff
    except Exception:
        h3 = False

    # H4: J_f(a) is invertible
    h4 = False
    try:
        if h3:
            det_J = J_a.det()
            if float(abs(det_J.evalf())) > 1e-9:
                h4 = True
    except Exception:
        h4 = False

    # neg_Q: f^{-1} is NOT differentiable at f(a), OR its Jacobian matrix is NOT (J_f(a))^{-1}
    neg_q = False
    try:
        if not h3 or not h4:
            neg_q = True
        else:
            is_locally_injective = True
            if n == 1:
                x = vars[0]
                df = sp.diff(f_expr[0], x)
                signs = set()
                for eps_val in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, -1e-2, -1e-3, -1e-4, -1e-5, -1e-6]:
                    try:
                        v = float(sp.re(df.subs(x, float(sp.re(sp.sympify(a[0]).evalf())) + eps_val).evalf()))
                        if v > 1e-9:
                            signs.add(1)
                        elif v < -1e-9:
                            signs.add(-1)
                    except Exception:
                        pass
                if len(signs) > 1:
                    is_locally_injective = False
            else:
                det_J_expr = J.det()
                signs = set()
                dirs = list(itertools.product([-1, 0, 1], repeat=n))
                dirs.remove(tuple([0]*n))
                for eps_val in [1e-3, 1e-5]:
                    for d in dirs:
                        norm = sum(x**2 for x in d)**0.5
                        pt = [float(sp.re(sp.sympify(a[i]).evalf())) + (x/norm)*eps_val for i, x in enumerate(d)]
                        try:
                            v = float(sp.re(det_J_expr.subs(zip(vars, pt)).evalf()))
                            if v > 1e-9:
                                signs.add(1)
                            elif v < -1e-9:
                                signs.add(-1)
                        except Exception:
                            pass
                if len(signs) > 1:
                    is_locally_injective = False

            if not is_locally_injective:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f is continuous and injective on U",
    "H_3: f is differentiable at a in U",
    "H_4: The Jacobian matrix J_f(a) is invertible",
    "¬Q: The inverse function f^{-1} is NOT differentiable at f(a), OR its Jacobian matrix is NOT (J_f(a))^{-1}"
]

N_HYP = 4
NEG_Q_INDEX = 4