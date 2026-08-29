import sympy as sp
import math
import itertools
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: U is an open subset of ℝ^n
    try:
        vars_list = list(witness['vars'])
        a_list = list(witness['a'])
        if len(vars_list) != len(a_list) or len(vars_list) == 0:
            h1 = False
        else:
            for val in a_list:
                float(val)
            h1 = True
    except Exception:
        h1 = False

    # H_2: f: U → ℝ^m is a function
    try:
        f_raw = witness['f']
        if isinstance(f_raw, sp.MatrixBase):
            f_exprs = list(f_raw)
        else:
            f_exprs = list(f_raw)
            
        if not isinstance(f_exprs, list) or len(f_exprs) == 0:
            h2 = False
        else:
            h2 = True
            for expr in f_exprs:
                if not isinstance(expr, sp.Expr) and not isinstance(expr, (int, float)):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: f is Fréchet differentiable at a
    try:
        f_raw = witness['f']
        if isinstance(f_raw, sp.MatrixBase):
            f_exprs = list(f_raw)
        else:
            f_exprs = list(f_raw)
            
        vars_list = list(witness['vars'])
        a_list = list(witness['a'])
        
        L_raw = witness['L']
        if isinstance(L_raw, sp.MatrixBase):
            L = L_raw.tolist()
        else:
            L = list(L_raw)
            
        n = len(vars_list)
        m = len(f_exprs)
        
        if len(L) != m:
            h3 = False
        else:
            h3_valid = True
            for row in L:
                if len(list(row)) != n:
                    h3_valid = False
                    break
            
            if h3_valid:
                # Check if L matches the limit-based partial derivatives
                for i in range(m):
                    for j in range(n):
                        t = sp.Symbol('t', real=True)
                        a_plus_t = list(a_list)
                        a_plus_t[j] = a_plus_t[j] + t
                        
                        expr = sp.sympify(f_exprs[i])
                        expr_t = expr.subs(zip(vars_list, a_plus_t))
                        expr_a = expr.subs(zip(vars_list, a_list))
                        
                        diff_limit = sp.limit((expr_t - expr_a) / t, t, 0)
                        if not diff_limit.is_real or diff_limit.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                            h3_valid = False
                            break
                        if abs(float(diff_limit) - float(L[i][j])) > 1e-5:
                            h3_valid = False
                            break
                    if not h3_valid:
                        break
                
                if not h3_valid:
                    h3 = False
                else:
                    # Check if partial derivatives are continuous at a
                    continuous_pd = True
                    for i in range(m):
                        expr = sp.sympify(f_exprs[i])
                        for j in range(n):
                            df = sp.diff(expr, vars_list[j])
                            val = df.subs(zip(vars_list, a_list))
                            if not val.is_real or val.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                                continuous_pd = False
                                break
                        if not continuous_pd:
                            break
                            
                    if continuous_pd:
                        h3 = True
                    else:
                        # Fallback to numerical check for Fréchet differentiability
                        f_funcs = [sp.lambdify(vars_list, sp.sympify(expr), 'math') for expr in f_exprs]
                        def eval_f(x):
                            return [float(f_funcs[i](*x)) for i in range(m)]
                            
                        fa = eval_f(a_list)
                        scale = 1e-5
                        num_valid = True
                        
                        dirs = []
                        for k in range(n):
                            d = [0]*n
                            d[k] = 1
                            dirs.append(d)
                            d2 = [0]*n
                            d2[k] = -1
                            dirs.append(d2)
                        
                        count = 0
                        for p in itertools.product([-1, 1], repeat=n):
                            dirs.append(list(p))
                            count += 1
                            if count > 100:
                                break
                                
                        if n >= 2:
                            dirs.append([1, 2] + [0]*(n-2))
                            dirs.append([2, -1] + [0]*(n-2))
                            
                        for d in dirs:
                            norm = math.sqrt(sum(x**2 for x in d))
                            if norm == 0: continue
                            h = [x / norm * scale for x in d]
                            
                            x = [a_list[k] + h[k] for k in range(n)]
                            try:
                                fx = eval_f(x)
                            except Exception:
                                num_valid = False
                                break
                                
                            Lh = [sum(float(L[i][k]) * h[k] for k in range(n)) for i in range(m)]
                            err = [fx[i] - fa[i] - Lh[i] for i in range(m)]
                            err_norm = math.sqrt(sum(e**2 for e in err))
                            
                            if err_norm / scale > 1e-2:
                                num_valid = False
                                break
                        h3 = num_valid
            else:
                h3 = False
    except Exception:
        h3 = False

    # ¬Q: Partial derivatives do not exist at a, or the Jacobian matrix does not represent the total derivative
    try:
        f_raw = witness['f']
        if isinstance(f_raw, sp.MatrixBase):
            f_exprs = list(f_raw)
        else:
            f_exprs = list(f_raw)
            
        vars_list = list(witness['vars'])
        a_list = list(witness['a'])
        
        L_raw = witness['L']
        if isinstance(L_raw, sp.MatrixBase):
            L = L_raw.tolist()
        else:
            L = list(L_raw)
            
        n = len(vars_list)
        m = len(f_exprs)
        
        neg_q = False
        for i in range(m):
            for j in range(n):
                t = sp.Symbol('t', real=True)
                a_plus_t = list(a_list)
                a_plus_t[j] = a_plus_t[j] + t
                
                expr = sp.sympify(f_exprs[i])
                expr_t = expr.subs(zip(vars_list, a_plus_t))
                expr_a = expr.subs(zip(vars_list, a_list))
                
                diff_limit = sp.limit((expr_t - expr_a) / t, t, 0)
                
                if not diff_limit.is_real or diff_limit.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    neg_q = True
                    break
                    
                if abs(float(diff_limit) - float(L[i][j])) > 1e-5:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open subset of ℝ^n",
    "H_2: f: U → ℝ^m is a function",
    "H_3: f is Fréchet differentiable at a",
    "¬Q: Partial derivatives do not exist at a, or the Jacobian matrix does not represent the total derivative"
]

N_HYP = 3
NEG_Q_INDEX = 3