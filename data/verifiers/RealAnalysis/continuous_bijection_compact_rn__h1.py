import sympy
from sympy import Symbol, Interval, Union, Piecewise, S, limit, oo, Limit
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# For this Real Analysis theorem, we define standard real variables and sequence indices.
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    """
    Expected witness format:
    witness = {
        'domain_sympy': sympy.Set,
        'f_sympy': sympy.Expr or tuple of sympy.Expr,
        'var_sympy': sympy.Symbol,
        'x_0_sympy': sympy.Expr (point in domain),
        'x_seq_sympy': sympy.Expr (sequence parameterized by n),
        'n_sympy': sympy.Symbol,
        'domain_z3': function taking a z3.Real and returning a z3.Bool,
        'f_z3': function taking a z3.Real and returning a z3.Real or list of z3.Reals
    }
    """
    # H_1: f is continuous on K
    h1_ok = False
    try:
        from sympy.calculus.util import continuous_domain
        domain_set = witness['domain_sympy']
        f_expr = witness['f_sympy']
        var = witness['var_sympy']
        
        if isinstance(f_expr, (list, tuple)):
            h1_ok = True
            for expr in f_expr:
                cd = continuous_domain(expr, var, S.Reals)
                if not domain_set.is_subset(cd):
                    h1_ok = False
                    break
        else:
            cd = continuous_domain(f_expr, var, S.Reals)
            h1_ok = bool(domain_set.is_subset(cd))
    except Exception:
        h1_ok = False

    # H_2: f is injective on K
    h2_ok = False
    try:
        domain_z3 = witness['domain_z3']
        f_z3 = witness['f_z3']
        
        zx = z3.Real('x')
        zy = z3.Real('y')
        
        solver = z3.Solver()
        solver.add(domain_z3(zx))
        solver.add(domain_z3(zy))
        
        fx = f_z3(zx)
        fy = f_z3(zy)
        if isinstance(fx, (list, tuple)):
            for fx_i, fy_i in zip(fx, fy):
                solver.add(fx_i == fy_i)
        else:
            solver.add(fx == fy)
            
        solver.add(zx != zy)
        
        # Set timeout to ensure fast execution
        solver.set("timeout", 2000)
        res = solver.check()
        if res == z3.unsat:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: f^{-1} is not continuous on f(K)
    neg_q_ok = False
    try:
        domain_set = witness['domain_sympy']
        f_expr = witness['f_sympy']
        var = witness['var_sympy']
        x_0 = witness['x_0_sympy']
        x_seq = witness['x_seq_sympy']
        seq_n = witness['n_sympy']
        
        def is_true(cond):
            if cond in (True, S.true): return True
            try:
                if bool(cond): return True
            except Exception:
                pass
            try:
                if bool(cond.simplify()): return True
            except Exception:
                pass
            return False

        # 1. x_0 is in K
        if is_true(domain_set.contains(x_0)):
            # 2. x_n is in K for large n
            in_domain = False
            for test_n in [100, 1000, 10000]:
                if is_true(domain_set.contains(x_seq.subs(seq_n, test_n))):
                    in_domain = True
                    break
            
            if in_domain:
                # 3. lim f(x_n) == f(x_0)
                lim_f_ok = True
                if isinstance(f_expr, (list, tuple)):
                    f_x_0 = [expr.subs(var, x_0) for expr in f_expr]
                    for i, expr in enumerate(f_expr):
                        f_x_n = expr.subs(var, x_seq)
                        lim_f = limit(f_x_n, seq_n, oo)
                        if isinstance(lim_f, Limit) or lim_f.has(Limit):
                            val = float(f_x_n.subs(seq_n, 10000))
                            if abs(val - float(f_x_0[i])) > 1e-3:
                                lim_f_ok = False
                                break
                        else:
                            try:
                                diff = float(abs(lim_f - f_x_0[i]))
                                if diff > 1e-7:
                                    lim_f_ok = False
                                    break
                            except Exception:
                                if lim_f != f_x_0[i]:
                                    lim_f_ok = False
                                    break
                else:
                    f_x_n = f_expr.subs(var, x_seq)
                    lim_f = limit(f_x_n, seq_n, oo)
                    f_x_0 = f_expr.subs(var, x_0)
                    if isinstance(lim_f, Limit) or lim_f.has(Limit):
                        val = float(f_x_n.subs(seq_n, 10000))
                        if abs(val - float(f_x_0)) > 1e-3:
                            lim_f_ok = False
                    else:
                        try:
                            diff = float(abs(lim_f - f_x_0))
                            if diff > 1e-7:
                                lim_f_ok = False
                        except Exception:
                            if lim_f != f_x_0:
                                lim_f_ok = False
                
                if lim_f_ok:
                    # 4. lim x_n != x_0  (which means f^{-1} is discontinuous at f(x_0))
                    lim_x = limit(x_seq, seq_n, oo)
                    if isinstance(lim_x, Limit) or lim_x.has(Limit):
                        val = float(x_seq.subs(seq_n, 10000))
                        if abs(val - float(x_0)) > 1e-3:
                            neg_q_ok = True
                    else:
                        try:
                            diff = float(abs(lim_x - x_0))
                            if diff > 1e-7:
                                neg_q_ok = True
                        except Exception:
                            if lim_x != x_0:
                                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is continuous on K",
    "H_2: f is injective on K",
    "¬Q: f^{-1} is not continuous on f(K)"
]

N_HYP = 2
NEG_Q_INDEX = 2