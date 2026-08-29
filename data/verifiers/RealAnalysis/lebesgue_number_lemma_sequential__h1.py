import sympy
import z3

# Top-level setup
Reals = sympy.S.Reals

CONDITION_LABELS = [
    "H_1: U is an open cover of X",
    "not Q: There is no Lebesgue number for the cover U"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_open_set(s):
    try:
        if getattr(s, 'is_open', None) is True:
            return True
    except Exception:
        pass
    if isinstance(s, sympy.Union):
        return all(is_open_set(arg) for arg in s.args)
    if isinstance(s, sympy.Intersection):
        return all(is_open_set(arg) for arg in s.args)
    if isinstance(s, sympy.Interval):
        return s.left_open and s.right_open
    if s == sympy.S.Reals:
        return True
    if isinstance(s, sympy.Complement):
        A, B = s.args
        if is_open_set(A) and isinstance(B, sympy.FiniteSet):
            return True
    return False

def set_to_z3(s, x):
    if isinstance(s, sympy.Interval):
        conds = []
        if s.start != sympy.S.NegativeInfinity:
            val = float(s.start)
            if s.left_open:
                conds.append(x > val)
            else:
                conds.append(x >= val)
        if s.end != sympy.S.Infinity:
            val = float(s.end)
            if s.right_open:
                conds.append(x < val)
            else:
                conds.append(x <= val)
        if not conds:
            return z3.BoolVal(True)
        if len(conds) == 1:
            return conds[0]
        return z3.And(*conds)
    elif isinstance(s, sympy.Union):
        args = [set_to_z3(arg, x) for arg in s.args]
        return z3.Or(*args) if args else z3.BoolVal(False)
    elif isinstance(s, sympy.Intersection):
        args = [set_to_z3(arg, x) for arg in s.args]
        return z3.And(*args) if args else z3.BoolVal(True)
    elif isinstance(s, sympy.EmptySet):
        return z3.BoolVal(False)
    elif s == sympy.S.Reals or isinstance(s, sympy.UniversalSet):
        return z3.BoolVal(True)
    elif isinstance(s, sympy.Complement):
        return z3.And(set_to_z3(s.args[0], x), z3.Not(set_to_z3(s.args[1], x)))
    elif isinstance(s, sympy.FiniteSet):
        args = [x == float(arg) for arg in s.args]
        return z3.Or(*args) if args else z3.BoolVal(False)
    else:
        raise ValueError(f"Unsupported set: {s}")

def conditions(witness):
    try:
        X, U = witness
    except Exception:
        return [False, False]
    
    h1_ok = False
    try:
        if isinstance(U, (list, tuple)) and all(isinstance(u, sympy.Set) for u in U) and isinstance(X, sympy.Set):
            all_open = all(is_open_set(u) for u in U)
            if all_open:
                x_var = z3.Real('x')
                X_z3 = set_to_z3(X, x_var)
                U_z3 = [set_to_z3(u, x_var) for u in U]
                
                if not U:
                    cover_cond = z3.ForAll(x_var, z3.Not(X_z3))
                else:
                    cover_cond = z3.ForAll(x_var, z3.Implies(X_z3, z3.Or(*U_z3)))
                
                solver = z3.Solver()
                solver.set("timeout", 2000)
                solver.add(z3.Not(cover_cond))
                if solver.check() == z3.unsat:
                    h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        delta = z3.Real('delta')
        x_var = z3.Real('x')
        y_var = z3.Real('y')
        
        X_z3_x = set_to_z3(X, x_var)
        X_z3_y = set_to_z3(X, y_var)
        
        abs_diff = z3.If(y_var - x_var >= 0, y_var - x_var, x_var - y_var)
        
        exists_U_conds = []
        for u in U:
            U_z3_y = set_to_z3(u, y_var)
            ball_subset = z3.ForAll(y_var, z3.Implies(
                z3.And(X_z3_y, abs_diff < delta),
                U_z3_y
            ))
            exists_U_conds.append(ball_subset)
            
        if not U:
            exists_U = z3.BoolVal(False)
        else:
            exists_U = z3.Or(*exists_U_conds)
            
        forall_x = z3.ForAll(x_var, z3.Implies(X_z3_x, exists_U))
        conclusion = z3.Exists(delta, z3.And(delta > 0, forall_x))
        
        solver = z3.Solver()
        solver.set("timeout", 2000)
        solver.add(conclusion)
        if solver.check() == z3.unsat:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]