import sympy
from sympy import Symbol, Interval, S, Abs, solveset, Eq, Union, Intersection
from sympy.calculus.util import function_range
import z3

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
y = Symbol('y', real=True)

CONDITION_LABELS = [
    "H_1: f maps X to X",
    "H_2: f is a contraction mapping on X (exists L in [0, 1) such that d(f(x), f(y)) <= L * d(x, y))",
    "¬Q: f does not have a unique fixed point in X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Try sympy evaluation first
    try:
        if isinstance(witness[0], sympy.Set):
            if len(witness) == 2:
                domain, f_in = witness
            else:
                domain, d_in, f_in = witness
                
            if domain.is_empty:
                return [False, False, False]
                
            if callable(f_in):
                f = f_in(x)
            else:
                f = f_in
                
            h1_ok = False
            try:
                rng = function_range(f, x, domain)
                if rng.is_subset(domain):
                    h1_ok = True
            except Exception:
                pass

            if not h1_ok:
                try:
                    if isinstance(domain, sympy.Interval):
                        inf_val = domain.inf
                        sup_val = domain.sup
                        
                        if inf_val != sympy.S.NegativeInfinity:
                            if domain.left_open:
                                viol_lower = sympy.solveset(f <= inf_val, x, domain)
                            else:
                                viol_lower = sympy.solveset(f < inf_val, x, domain)
                        else:
                            viol_lower = sympy.S.EmptySet
                            
                        if sup_val != sympy.S.Infinity:
                            if domain.right_open:
                                viol_upper = sympy.solveset(f >= sup_val, x, domain)
                            else:
                                viol_upper = sympy.solveset(f > sup_val, x, domain)
                        else:
                            viol_upper = sympy.S.EmptySet
                            
                        if viol_lower.is_empty and viol_upper.is_empty:
                            h1_ok = True
                except Exception:
                    pass

            h2_ok = False
            try:
                df = sympy.diff(f, x)
                df_rng = function_range(df, x, domain)
                if df_rng.sup < 1 and df_rng.inf > -1:
                    h2_ok = True
            except Exception:
                pass

            if not h2_ok:
                try:
                    df = sympy.diff(f, x)
                    crit_points = sympy.solveset(sympy.diff(df, x), x, domain)
                    eval_points = set()
                    if isinstance(crit_points, sympy.FiniteSet):
                        eval_points.update(crit_points)
                    if isinstance(domain, sympy.Interval):
                        if domain.inf not in [sympy.S.NegativeInfinity, sympy.S.Infinity]:
                            eval_points.add(domain.inf)
                        if domain.sup not in [sympy.S.NegativeInfinity, sympy.S.Infinity]:
                            eval_points.add(domain.sup)
                    
                    max_val = -1
                    for p in eval_points:
                        try:
                            if p == sympy.S.Infinity:
                                val = sympy.limit(df, x, sympy.S.Infinity)
                            elif p == sympy.S.NegativeInfinity:
                                val = sympy.limit(df, x, sympy.S.NegativeInfinity)
                            else:
                                val = df.subs(x, p)
                            
                            val = abs(val)
                            if val == sympy.S.Infinity:
                                max_val = float('inf')
                            elif val.is_real:
                                val_f = float(val)
                                if val_f > max_val:
                                    max_val = val_f
                        except Exception:
                            pass
                    
                    if 0 <= max_val < 1:
                        h2_ok = True
                    else:
                        try:
                            if df.is_constant() and abs(float(df)) < 1:
                                h2_ok = True
                        except Exception:
                            pass
                except Exception:
                    pass

            neg_q_ok = False
            try:
                fixed_points = sympy.solveset(sympy.Eq(f, x), x, domain)
                if isinstance(fixed_points, sympy.FiniteSet):
                    if len(fixed_points) != 1:
                        neg_q_ok = True
                elif fixed_points.is_empty:
                    neg_q_ok = True
                elif isinstance(fixed_points, sympy.Set) and not isinstance(fixed_points, sympy.ConditionSet):
                    neg_q_ok = True
            except Exception:
                pass

            return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        pass

    # Try Z3 evaluation if sympy fails or witness is Z3-based
    try:
        if len(witness) == 2:
            domain, f_in = witness
            d = lambda a, b: z3.If(a >= b, a - b, b - a)
        elif len(witness) == 3:
            domain, d, f_in = witness
        else:
            return [False, False, False]
            
        f = f_in
        
        zx, zy, zL, zx_star, zy_star = z3.Reals('x y L x_star y_star')
        
        solver_empty = z3.Solver()
        solver_empty.set("timeout", 1000)
        solver_empty.add(domain(zx))
        if solver_empty.check() == z3.unsat:
            return [False, False, False]
        
        solver1 = z3.Solver()
        solver1.set("timeout", 1000)
        solver1.add(domain(zx))
        solver1.add(z3.Not(domain(f(zx))))
        h1_ok = (solver1.check() == z3.unsat)
        
        solver2 = z3.Solver()
        solver2.set("timeout", 2000)
        solver2.add(zL >= 0, zL < 1)
        solver2.add(z3.ForAll([zx, zy], z3.Implies(z3.And(domain(zx), domain(zy)), d(f(zx), f(zy)) <= zL * d(zx, zy))))
        res2 = solver2.check()
        if res2 == z3.sat:
            h2_ok = True
        else:
            h2_ok = False
            for test_L in [0.5, 0.9, 0.99]:
                s_test = z3.Solver()
                s_test.set("timeout", 1000)
                s_test.add(z3.ForAll([zx, zy], z3.Implies(z3.And(domain(zx), domain(zy)), d(f(zx), f(zy)) <= test_L * d(zx, zy))))
                if s_test.check() == z3.sat:
                    h2_ok = True
                    break
        
        solver3 = z3.Solver()
        solver3.set("timeout", 1000)
        solver3.add(domain(zx_star), f(zx_star) == zx_star)
        res = solver3.check()
        if res == z3.unsat:
            neg_q_ok = True
        elif res == z3.sat:
            solver4 = z3.Solver()
            solver4.set("timeout", 1000)
            solver4.add(domain(zx_star), f(zx_star) == zx_star)
            solver4.add(domain(zy_star), f(zy_star) == zy_star)
            solver4.add(zx_star != zy_star)
            neg_q_ok = (solver4.check() == z3.sat)
        else:
            neg_q_ok = False
            
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        pass

    return [False, False, False]