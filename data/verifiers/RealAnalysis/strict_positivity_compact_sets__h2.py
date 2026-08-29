import sympy
from sympy import Interval, Piecewise, Symbol, Eq, Union, Intersection, FiniteSet, Complement, ProductSet
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is a compact subset of R^n",
    "H_2: For all x in K, f(x) > 0",
    "¬Q: There does not exist c > 0 such that f(x) >= c for all x in K"
]
N_HYP = 2
NEG_Q_INDEX = 2

def is_compact(K):
    if not isinstance(K, sympy.Set): return False
    is_real_subset = False
    if K.is_subset(sympy.S.Reals):
        is_real_subset = True
    elif isinstance(K, ProductSet):
        if all(arg.is_subset(sympy.S.Reals) for arg in K.args):
            is_real_subset = True
    if not is_real_subset:
        return False
    
    if isinstance(K, ProductSet):
        if not all(arg.is_closed for arg in K.args): return False
        if not all(arg.is_bounded for arg in K.args): return False
    else:
        if not K.is_closed: return False
        if not K.is_bounded: return False
    return True

def get_boundary_points(K):
    pts = set()
    if isinstance(K, Interval):
        pts.add(float(K.start))
        pts.add(float(K.end))
    elif isinstance(K, Union) or isinstance(K, Intersection):
        for arg in K.args:
            pts.update(get_boundary_points(arg))
    elif isinstance(K, FiniteSet):
        for arg in K.args:
            pts.add(float(arg))
    elif isinstance(K, Complement):
        pts.update(get_boundary_points(K.args[0]))
        pts.update(get_boundary_points(K.args[1]))
    return pts

def get_sample_points(K):
    try:
        inf = float(K.inf)
        sup = float(K.sup)
    except Exception:
        return []
    
    pts = set()
    pts.add(inf)
    pts.add(sup)
    n_samples = 10000
    for i in range(1, n_samples):
        pts.add(inf + (sup - inf) * i / n_samples)
        
    try:
        boundaries = get_boundary_points(K)
        for b in boundaries:
            pts.add(b)
            pts.add(b + 1e-7)
            pts.add(b - 1e-7)
    except Exception:
        pass
        
    if inf < 0 < sup:
        pts.add(0.0)
        pts.add(1e-7)
        pts.add(-1e-7)
        
    valid_pts = []
    for p in pts:
        try:
            if K.contains(p) == sympy.S.true:
                valid_pts.append(p)
        except Exception:
            pass
    return valid_pts

def fallback_H2(K, f, x_sym):
    pts = get_sample_points(K)
    evaluated_any = False
    for p in pts:
        try:
            val = float(f.subs(x_sym, p).evalf())
            evaluated_any = True
            if val <= 0:
                return False
        except Exception:
            pass
    return evaluated_any

def fallback_H2_func(K, f):
    pts = get_sample_points(K)
    evaluated_any = False
    for p in pts:
        try:
            val = float(f(p))
            evaluated_any = True
            if val <= 0:
                return False
        except Exception:
            pass
    return evaluated_any

def fallback_neg_Q(K, f, x_sym):
    pts = get_sample_points(K)
    min_val = float('inf')
    evaluated_any = False
    for p in pts:
        try:
            val = float(f.subs(x_sym, p).evalf())
            evaluated_any = True
            if val < min_val:
                min_val = val
        except Exception:
            pass
    if not evaluated_any:
        return False
    return min_val <= 1e-3

def fallback_neg_Q_func(K, f):
    pts = get_sample_points(K)
    min_val = float('inf')
    evaluated_any = False
    for p in pts:
        try:
            val = float(f(p))
            evaluated_any = True
            if val < min_val:
                min_val = val
        except Exception:
            pass
    if not evaluated_any:
        return False
    return min_val <= 1e-3

def set_to_z3(S, z3_var):
    if isinstance(S, Interval):
        conds = []
        if S.left_open:
            if S.start != -sympy.oo:
                conds.append(z3_var > float(S.start))
        else:
            if S.start != -sympy.oo:
                conds.append(z3_var >= float(S.start))
        if S.right_open:
            if S.end != sympy.oo:
                conds.append(z3_var < float(S.end))
        else:
            if S.end != sympy.oo:
                conds.append(z3_var <= float(S.end))
        if not conds:
            return z3.BoolVal(True)
        return z3.And(*conds)
    elif isinstance(S, Union):
        return z3.Or(*[set_to_z3(arg, z3_var) for arg in S.args])
    elif isinstance(S, Intersection):
        return z3.And(*[set_to_z3(arg, z3_var) for arg in S.args])
    elif isinstance(S, FiniteSet):
        return z3.Or(*[z3_var == float(arg) for arg in S.args])
    elif isinstance(S, Complement):
        return z3.And(set_to_z3(S.args[0], z3_var), z3.Not(set_to_z3(S.args[1], z3_var)))
    else:
        raise ValueError(f"Unsupported sympy set: {S}")

def sympy_to_z3(expr, z3_vars):
    if isinstance(expr, Symbol):
        if expr in z3_vars:
            return z3_vars[expr]
        else:
            raise ValueError(f"Unknown symbol {expr}")
    elif isinstance(expr, (int, float)):
        return z3.RealVal(expr)
    elif isinstance(expr, sympy.Rational):
        return z3.RealVal(int(expr.p)) / z3.RealVal(int(expr.q))
    elif isinstance(expr, sympy.Number):
        return z3.RealVal(float(expr))
    elif isinstance(expr, sympy.Add):
        res = sympy_to_z3(expr.args[0], z3_vars)
        for arg in expr.args[1:]:
            res = res + sympy_to_z3(arg, z3_vars)
        return res
    elif isinstance(expr, sympy.Mul):
        res = sympy_to_z3(expr.args[0], z3_vars)
        for arg in expr.args[1:]:
            res = res * sympy_to_z3(arg, z3_vars)
        return res
    elif isinstance(expr, sympy.Pow):
        base = sympy_to_z3(expr.args[0], z3_vars)
        exp = sympy_to_z3(expr.args[1], z3_vars)
        return base ** exp
    elif isinstance(expr, Piecewise):
        res = z3.RealVal(0)
        for e, c in reversed(expr.args):
            if c == sympy.S.true or c is True:
                res = sympy_to_z3(e, z3_vars)
            else:
                z3_c = sympy_to_z3(c, z3_vars)
                z3_e = sympy_to_z3(e, z3_vars)
                res = z3.If(z3_c, z3_e, res)
        return res
    elif isinstance(expr, sympy.Relational):
        lhs = sympy_to_z3(expr.lhs, z3_vars)
        rhs = sympy_to_z3(expr.rhs, z3_vars)
        if isinstance(expr, sympy.StrictGreaterThan): return lhs > rhs
        if isinstance(expr, sympy.StrictLessThan): return lhs < rhs
        if isinstance(expr, sympy.GreaterThan): return lhs >= rhs
        if isinstance(expr, sympy.LessThan): return lhs <= rhs
        if isinstance(expr, sympy.Eq): return lhs == rhs
        if isinstance(expr, sympy.Ne): return lhs != rhs
    elif isinstance(expr, sympy.And):
        return z3.And(*[sympy_to_z3(arg, z3_vars) for arg in expr.args])
    elif isinstance(expr, sympy.Or):
        return z3.Or(*[sympy_to_z3(arg, z3_vars) for arg in expr.args])
    elif isinstance(expr, sympy.Not):
        return z3.Not(sympy_to_z3(expr.args[0], z3_vars))
    elif expr == sympy.S.true or expr is True:
        return z3.BoolVal(True)
    elif expr == sympy.S.false or expr is False:
        return z3.BoolVal(False)
    else:
        if expr.func == sympy.Abs:
            arg = sympy_to_z3(expr.args[0], z3_vars)
            return z3.If(arg >= 0, arg, -arg)
        raise ValueError(f"Unsupported sympy expression: {expr} of type {type(expr)}")

def conditions(witness):
    try:
        if len(witness) == 3:
            K, f, x_sym = witness
        elif len(witness) == 2:
            K, f = witness
            if isinstance(f, sympy.Expr):
                free = f.free_symbols
                if len(free) != 1:
                    x_sym = Symbol('x')
                else:
                    x_sym = list(free)[0]
            else:
                x_sym = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    h1_ok = False
    try:
        h1_ok = is_compact(K)
    except Exception:
        pass

    h2_ok = False
    try:
        if isinstance(f, sympy.Expr) and x_sym is not None:
            z3_x = z3.Real('x')
            z3_K = set_to_z3(K, z3_x)
            z3_f = sympy_to_z3(f, {x_sym: z3_x})
            solver = z3.Solver()
            solver.add(z3_K)
            solver.add(z3_f <= 0)
            res = solver.check()
            if res == z3.unsat:
                h2_ok = True
            elif res == z3.sat:
                h2_ok = False
            else:
                h2_ok = fallback_H2(K, f, x_sym)
        else:
            h2_ok = fallback_H2_func(K, f)
    except Exception:
        if isinstance(f, sympy.Expr) and x_sym is not None:
            h2_ok = fallback_H2(K, f, x_sym)
        else:
            h2_ok = fallback_H2_func(K, f)

    neg_q_ok = False
    try:
        if isinstance(f, sympy.Expr) and x_sym is not None:
            z3_x = z3.Real('x')
            z3_K = set_to_z3(K, z3_x)
            z3_f = sympy_to_z3(f, {x_sym: z3_x})
            c = z3.Real('c')
            solver = z3.Solver()
            forall_cond = z3.ForAll([z3_x], z3.Implies(z3_K, z3_f >= c))
            solver.add(c > 0)
            solver.add(forall_cond)
            res = solver.check()
            if res == z3.unsat:
                neg_q_ok = True
            elif res == z3.sat:
                neg_q_ok = False
            else:
                neg_q_ok = fallback_neg_Q(K, f, x_sym)
        else:
            neg_q_ok = fallback_neg_Q_func(K, f)
    except Exception:
        if isinstance(f, sympy.Expr) and x_sym is not None:
            neg_q_ok = fallback_neg_Q(K, f, x_sym)
        else:
            neg_q_ok = fallback_neg_Q_func(K, f)

    return [h1_ok, h2_ok, neg_q_ok]