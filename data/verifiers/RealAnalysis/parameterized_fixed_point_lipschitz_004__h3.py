import sympy as sp
import z3

# Top-level setup: named object bindings that the witness expression may reference.
x, lam = sp.symbols('x lam', real=True)
lambda_ = lam

def z3_abs(val):
    if isinstance(val, (int, float)):
        return abs(val)
    return z3.If(val >= 0, val, -val)

def sympy_to_z3(expr, x_z3, lam_z3):
    if callable(expr):
        return expr(x_z3, lam_z3)
    
    def convert(e):
        if isinstance(e, sp.Symbol):
            if e.name == 'x': return x_z3
            if e.name in ['lam', 'lambda', 'lambda_']: return lam_z3
            raise ValueError(f"Unknown symbol {e}")
        elif isinstance(e, sp.Number):
            return float(e)
        elif isinstance(e, sp.Add):
            return z3.Sum(*[convert(arg) for arg in e.args])
        elif isinstance(e, sp.Mul):
            res = convert(e.args[0])
            for arg in e.args[1:]:
                res *= convert(arg)
            return res
        elif isinstance(e, sp.Pow):
            return convert(e.args[0]) ** convert(e.args[1])
        elif isinstance(e, sp.Abs):
            arg = convert(e.args[0])
            return z3_abs(arg)
        else:
            try:
                return float(e)
            except Exception:
                raise ValueError(f"Unsupported expr: {e}")
    return convert(expr)

def in_domain(var, bounds):
    if bounds is None:
        return z3.BoolVal(True)
    conds = []
    if bounds[0] is not None:
        conds.append(var >= float(bounds[0]))
    if bounds[1] is not None:
        conds.append(var <= float(bounds[1]))
    if len(conds) == 0:
        return z3.BoolVal(True)
    elif len(conds) == 1:
        return conds[0]
    else:
        return z3.And(*conds)

def check_z3_valid(claim, timeout=1000):
    solver = z3.Solver()
    solver.set("timeout", timeout)
    solver.add(z3.Not(claim))
    res = solver.check()
    return res == z3.unsat

def check_closed_formula(formula, timeout=1000):
    solver = z3.Solver()
    solver.set("timeout", timeout)
    solver.add(formula)
    res = solver.check()
    if res == z3.sat:
        return True
    elif res == z3.unsat:
        return False
    else:
        raise Exception("z3 unknown")

def conditions(witness) -> list[bool]:
    """
    witness can be a dictionary:
      {'T': expr_or_callable, 'L': float, 'k': float, 'X': (min, max), 'Lambda': (min, max)}
    or a tuple:
      (T, L, k)  # assumes X and Lambda are (-oo, oo)
      (T, L, k, X_bounds, Lambda_bounds)
    """
    try:
        if isinstance(witness, dict):
            T_expr = witness['T']
            L = float(witness['L'])
            k = float(witness['k'])
            X_bounds = witness.get('X', None)
            Lambda_bounds = witness.get('Lambda', None)
        else:
            if len(witness) == 3:
                T_expr, L, k = witness
                X_bounds = None
                Lambda_bounds = None
            elif len(witness) == 5:
                T_expr, L, k, X_bounds, Lambda_bounds = witness
            else:
                return [False, False, False, False]
            L = float(L)
            k = float(k)
    except Exception:
        return [False, False, False, False]

    def valid_bounds(b):
        if b is None: return True
        if b[0] is not None and b[1] is not None:
            return float(b[0]) <= float(b[1])
        return True

    try:
        h1_ok = valid_bounds(X_bounds) and valid_bounds(Lambda_bounds)
    except Exception:
        h1_ok = False

    try:
        x_z3 = z3.Real('x')
        lam_z3 = z3.Real('lam')
        T_val = sympy_to_z3(T_expr, x_z3, lam_z3)
        
        claim_H2 = z3.Implies(
            z3.And(in_domain(x_z3, X_bounds), in_domain(lam_z3, Lambda_bounds)),
            in_domain(T_val, X_bounds)
        )
        h2_ok = check_z3_valid(z3.ForAll([x_z3, lam_z3], claim_H2))
    except Exception:
        h2_ok = False

    try:
        if L <= 0:
            h3_ok = False
        else:
            lam1_z3 = z3.Real('lam1')
            lam2_z3 = z3.Real('lam2')
            T1 = sympy_to_z3(T_expr, x_z3, lam1_z3)
            T2 = sympy_to_z3(T_expr, x_z3, lam2_z3)
            
            claim_H3 = z3.Implies(
                z3.And(
                    in_domain(x_z3, X_bounds),
                    in_domain(lam1_z3, Lambda_bounds),
                    in_domain(lam2_z3, Lambda_bounds)
                ),
                z3_abs(T1 - T2) <= L * z3_abs(lam1_z3 - lam2_z3)
            )
            h3_ok = check_z3_valid(z3.ForAll([x_z3, lam1_z3, lam2_z3], claim_H3))
    except Exception:
        h3_ok = False

    try:
        if k == 1:
            neg_Q = True
        else:
            lip_const = L / (1 - k)
            
            y_z3 = z3.Real('y')
            x1_z3 = z3.Real('x1')
            x2_z3 = z3.Real('x2')
            
            is_fp_x = z3.And(in_domain(x_z3, X_bounds), sympy_to_z3(T_expr, x_z3, lam_z3) == x_z3)
            is_fp_y = z3.And(in_domain(y_z3, X_bounds), sympy_to_z3(T_expr, y_z3, lam_z3) == y_z3)
            
            unique_fp_for_lam = z3.Exists([x_z3], z3.And(
                is_fp_x,
                z3.ForAll([y_z3], z3.Implies(is_fp_y, y_z3 == x_z3))
            ))
            
            all_lam_unique_fp = z3.ForAll([lam_z3], z3.Implies(in_domain(lam_z3, Lambda_bounds), unique_fp_for_lam))
            
            is_fp_x1 = z3.And(in_domain(x1_z3, X_bounds), sympy_to_z3(T_expr, x1_z3, lam1_z3) == x1_z3)
            is_fp_x2 = z3.And(in_domain(x2_z3, X_bounds), sympy_to_z3(T_expr, x2_z3, lam2_z3) == x2_z3)
            
            lip_cond = z3.Implies(
                z3.And(
                    in_domain(lam1_z3, Lambda_bounds),
                    in_domain(lam2_z3, Lambda_bounds),
                    is_fp_x1,
                    is_fp_x2
                ),
                z3_abs(x1_z3 - x2_z3) <= lip_const * z3_abs(lam1_z3 - lam2_z3)
            )
            
            all_lip = z3.ForAll([lam1_z3, lam2_z3, x1_z3, x2_z3], lip_cond)
            
            conclusion = z3.And(all_lam_unique_fp, all_lip)
            conclusion_holds = check_closed_formula(conclusion)
            neg_Q = not conclusion_holds
    except Exception:
        neg_Q = False

    return [h1_ok, h2_ok, h3_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: X is a complete metric space and Lambda is a metric space",
    "H_2: T: X x Lambda -> X is a mapping",
    "H_3: T is Lipschitz continuous with respect to lambda with constant L > 0",
    "¬Q: The unique fixed point x*(lambda) is NOT Lipschitz continuous with constant L / (1 - k)"
]

N_HYP = 3
NEG_Q_INDEX = 3