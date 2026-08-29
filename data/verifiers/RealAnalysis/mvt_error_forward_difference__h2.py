import sympy
from sympy import Symbol, diff, solveset, Interval, S, simplify

# Top-level setup
t = Symbol('t', real=True)

def conditions(witness):
    try:
        f = witness.get('f')
        x_val = witness.get('x')
        h_val = witness.get('h')
        if f is None or x_val is None or h_val is None:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: h > 0
    try:
        h_ok = bool(h_val > 0)
    except Exception:
        h_ok = False
        
    # ¬Q: The conclusion fails (there does not exist c in (x, x+h) satisfying the equation)
    try:
        free_vars = f.free_symbols
        if len(free_vars) == 1:
            var = list(free_vars)[0]
        elif len(free_vars) == 0:
            var = t
        else:
            var = t
            
        f_prime = diff(f, var)
        f_double_prime = diff(f_prime, var)
        
        f_x = f.subs(var, x_val)
        f_x_h = f.subs(var, x_val + h_val)
        f_prime_x = f_prime.subs(var, x_val)
        
        LHS = (f_x_h - f_x) / h_val - f_prime_x
        LHS = simplify(LHS)
        
        # If LHS is undefined or infinite, the equation cannot be satisfied by any real c
        if not LHS.is_number or LHS.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo):
            neg_q = True
        else:
            target_f_double_prime = LHS * 2 / h_val
            eq = f_double_prime - target_f_double_prime
            
            if simplify(eq) == 0:
                neg_q = False
            else:
                neg_q = False
                try:
                    sols = solveset(eq, var, domain=Interval.open(x_val, x_val + h_val))
                    if sols is S.EmptySet:
                        neg_q = True
                    elif isinstance(sols, sympy.ConditionSet):
                        # Fallback to solve if solveset returns a ConditionSet
                        sols_solve = sympy.solve(eq, var)
                        if isinstance(sols_solve, list):
                            any_in_interval = False
                            for sol in sols_solve:
                                try:
                                    if sol.is_real is not False and bool(sol > x_val) and bool(sol < x_val + h_val):
                                        any_in_interval = True
                                        break
                                except Exception:
                                    pass
                            if not any_in_interval:
                                neg_q = True
                except Exception:
                    # Fallback to solve if solveset raises an exception
                    try:
                        sols_solve = sympy.solve(eq, var)
                        if isinstance(sols_solve, list):
                            any_in_interval = False
                            for sol in sols_solve:
                                try:
                                    if sol.is_real is not False and bool(sol > x_val) and bool(sol < x_val + h_val):
                                        any_in_interval = True
                                        break
                                except Exception:
                                    pass
                            if not any_in_interval:
                                neg_q = True
                    except Exception:
                        pass
    except Exception:
        neg_q = False
        
    return [h_ok, neg_q]

CONDITION_LABELS = [
    "H_1: h > 0",
    "¬Q: There does not exist c in (x, x+h) such that (f(x+h) - f(x))/h - f'(x) = (h/2)f''(c)"
]

N_HYP = 1
NEG_Q_INDEX = 1