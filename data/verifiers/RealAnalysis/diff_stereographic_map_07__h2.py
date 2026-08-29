import sympy
import z3
import math
import itertools
import functools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

x, y, z, t = sympy.symbols('x y z t', real=True)
x1, x2, x3, x4, x5 = sympy.symbols('x1 x2 x3 x4 x5', real=True)

def sort_key(sym):
    name = sym.name
    for i, c in enumerate(name):
        if c.isdigit():
            prefix = name[:i]
            suffix = name[i:]
            try:
                return (0, prefix, int(suffix))
            except ValueError:
                return (1, name, 0)
    return (1, name, 0)

def get_vars_and_xn(exprs):
    symbols = set()
    for e in exprs:
        if hasattr(e, 'free_symbols'):
            symbols.update(e.free_symbols)
    if not symbols:
        return [], None
    sorted_syms = sorted(list(symbols), key=sort_key)
    x_n_plus_1 = sorted_syms[-1]
    return sorted_syms, x_n_plus_1

def extract_exprs(witness):
    if isinstance(witness, dict):
        f = witness.get('f', witness.get('func', None))
        if f is None:
            for v in witness.values():
                if hasattr(v, 'free_symbols'):
                    f = v
                    break
            if f is None:
                f = witness
    elif isinstance(witness, (tuple, list)):
        if len(witness) > 0 and isinstance(witness[0], (int, str)):
            f = witness[-1]
        else:
            f = witness
    else:
        f = witness
        
    exprs = []
    if hasattr(f, '__iter__') and not isinstance(f, str):
        for item in f:
            exprs.append(item)
    else:
        exprs.append(f)
        
    return exprs

def translate_to_z3(e, z3_vars):
    if e.is_Integer:
        return int(e)
    if e.is_Rational:
        return int(e.p) / int(e.q)
    if e.is_Float:
        return float(e)
    if e.is_Symbol:
        return z3_vars[e.name]
    if e.is_Add:
        res = translate_to_z3(e.args[0], z3_vars)
        for arg in e.args[1:]:
            res += translate_to_z3(arg, z3_vars)
        return res
    if e.is_Mul:
        res = translate_to_z3(e.args[0], z3_vars)
        for arg in e.args[1:]:
            res *= translate_to_z3(arg, z3_vars)
        return res
    if e.is_Pow:
        base, exp = e.args
        if exp.is_Integer:
            b = translate_to_z3(base, z3_vars)
            e_int = int(exp)
            if e_int == 0:
                return 1
            elif e_int > 0:
                res = b
                for _ in range(e_int - 1):
                    res *= b
                return res
            else:
                res = b
                for _ in range(-e_int - 1):
                    res *= b
                return 1 / res
    raise ValueError(f"Unsupported: {e}")

def has_singularities_in_U(expr, vars_list, x_n_plus_1):
    if expr.has(sympy.Abs, sympy.Min, sympy.Max, sympy.sign, sympy.Piecewise,
                sympy.tan, sympy.sec, sympy.csc, sympy.cot, sympy.asin, sympy.acos):
        return True
    for v in vars_list:
        df = sympy.diff(expr, v)
        n, d = df.as_numer_denom()
        if d != 1:
            z3_res = None
            try:
                solver = z3.Solver()
                z3_vars = {var.name: z3.Real(var.name) for var in vars_list}
                z3_d = translate_to_z3(d, z3_vars)
                solver.add(z3_d == 0)
                if x_n_plus_1.name in z3_vars:
                    solver.add(z3_vars[x_n_plus_1.name] != 1)
                solver.set("timeout", 1000)
                res = solver.check()
                if res == z3.sat:
                    z3_res = True
                elif res == z3.unsat:
                    z3_res = False
            except Exception:
                pass
            
            if z3_res is not None:
                if z3_res:
                    return True
                else:
                    continue
            
            # Fallback to sympy
            try:
                d_sub = d.subs(x_n_plus_1, 0)
                if d_sub == 0:
                    return True
                roots = sympy.solve(d_sub, dict=True)
                for root in roots:
                    if all(val.is_real is not False for val in root.values()):
                        return True
                        
                d_sub2 = d.subs(x_n_plus_1, 2)
                if d_sub2 == 0:
                    return True
                roots2 = sympy.solve(d_sub2, dict=True)
                for root in roots2:
                    if all(val.is_real is not False for val in root.values()):
                        return True
            except Exception:
                pass
                
    return False

def conditions(witness):
    try:
        exprs = extract_exprs(witness)
        vars_list, x_n_plus_1 = get_vars_and_xn(exprs)
        
        # H_1: U = {x in R^{n+1} : x_{n+1} != 1}
        # This is a definition of the domain U. We verify the witness provides valid expressions.
        h1_ok = len(exprs) > 0 and all(hasattr(e, 'free_symbols') for e in exprs)
        
        # neg_Q: f is not differentiable on U
        neg_q_ok = False
        if h1_ok:
            for expr in exprs:
                if has_singularities_in_U(expr, vars_list, x_n_plus_1):
                    neg_q_ok = True
                    break
                    
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: U = {x in R^{n+1} : x_{n+1} != 1}",
    "¬Q: f is not differentiable on U"
]

N_HYP = 1
NEG_Q_INDEX = 1