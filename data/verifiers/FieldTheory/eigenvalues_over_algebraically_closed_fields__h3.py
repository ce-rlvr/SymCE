import sympy
import z3
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: V is a finite-dimensional non-zero vector space over K",
    "¬Q: T has no eigenvectors in V"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        K, X_syms, T_obj = witness
    except Exception:
        return [False, False, False]
        
    # H1: K is an algebraically closed field
    try:
        # In SymPy, CC is the complex field, which is algebraically closed.
        h1 = (K == sympy.CC)
    except Exception:
        h1 = False
        
    # H2: V is a finite-dimensional non-zero vector space over K
    try:
        h2 = (isinstance(X_syms, list) and len(X_syms) > 0 and 
              all(isinstance(sym, sympy.Symbol) for sym in X_syms) and
              len(set(X_syms)) == len(X_syms))
    except Exception:
        h2 = False
        
    neg_q = False
    try:
        if not (h1 and h2):
            return [h1, h2, False]
            
        n = len(X_syms)
        if isinstance(T_obj, sympy.MatrixBase):
            if T_obj.shape != (n, n):
                return [h1, h2, False]
            T_syms = [sum(T_obj[i, j] * X_syms[j] for j in range(n)) for i in range(n)]
        elif isinstance(T_obj, (list, tuple)):
            if len(T_obj) != n:
                return [h1, h2, False]
            T_syms = T_obj
        elif callable(T_obj):
            T_syms = T_obj(X_syms)
            if not isinstance(T_syms, (list, tuple)) or len(T_syms) != n:
                return [h1, h2, False]
        else:
            return [h1, h2, False]
            
        # Convert to Z3 and check for eigenvectors
        real_syms = []
        subs_dict = {}
        for sym in X_syms:
            xr = sympy.Symbol(sym.name + '_re', real=True)
            xi = sympy.Symbol(sym.name + '_im', real=True)
            real_syms.append((xr, xi))
            subs_dict[sym] = xr + sympy.I * xi
            
        T_real_im = []
        for t in T_syms:
            t_sub = sympy.sympify(t).subs(subs_dict)
            t_sub = sympy.expand_complex(t_sub)
            tr, ti = t_sub.as_real_imag()
            T_real_im.append((tr, ti))
            
        # Z3 variables
        var_map = {}
        z3_X = []
        for xr, xi in real_syms:
            zx_r = z3.Real(xr.name)
            zx_i = z3.Real(xi.name)
            var_map[xr] = zx_r
            var_map[xi] = zx_i
            z3_X.append((zx_r, zx_i))
            
        def sym_to_z3(expr):
            if expr.is_Symbol:
                if expr not in var_map:
                    raise ValueError(f"Unknown symbol: {expr}")
                return var_map[expr]
            elif expr.is_Integer:
                return z3.RealVal(int(expr))
            elif expr.is_Rational:
                return z3.RealVal(expr.p) / z3.RealVal(expr.q)
            elif expr.is_Float:
                return z3.RealVal(float(expr))
            elif expr == sympy.pi:
                return z3.RealVal(3.141592653589793)
            elif expr == sympy.E:
                return z3.RealVal(2.718281828459045)
            elif expr.is_Add:
                res = sym_to_z3(expr.args[0])
                for arg in expr.args[1:]:
                    res += sym_to_z3(arg)
                return res
            elif expr.is_Mul:
                res = sym_to_z3(expr.args[0])
                for arg in expr.args[1:]:
                    res *= sym_to_z3(arg)
                return res
            elif expr.is_Pow:
                base = sym_to_z3(expr.base)
                exp = sym_to_z3(expr.exp)
                return base ** exp
            else:
                raise ValueError(f"Unsupported: {expr.func}")
                
        solver = z3.Solver()
        
        # X != 0
        any_nonzero = z3.Or(*[z3.Or(x_var[0] != 0, x_var[1] != 0) for x_var in z3_X])
        solver.add(any_nonzero)
        
        lam_re = z3.Real('lam_re')
        lam_im = z3.Real('lam_im')
        
        for i in range(n):
            tr_expr, ti_expr = T_real_im[i]
            z3_tr = sym_to_z3(tr_expr)
            z3_ti = sym_to_z3(ti_expr)
            
            x_re, x_im = z3_X[i]
            
            rhs_re = lam_re * x_re - lam_im * x_im
            rhs_im = lam_re * x_im + lam_im * x_re
            
            solver.add(z3_tr == rhs_re)
            solver.add(z3_ti == rhs_im)
            
        solver.set("timeout", 2000)
        res = solver.check()
        
        if res == z3.unsat:
            neg_q = True
        else:
            neg_q = False
            
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]