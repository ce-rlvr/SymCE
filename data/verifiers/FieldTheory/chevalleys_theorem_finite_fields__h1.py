import sympy as sp
from sympy import symbols, Rational, Integer, Poly
from sympy.abc import x, y, z, w, u, v, a, b, c, d
import z3
import itertools
import math
import functools

CONDITION_LABELS = [
    "H_1: f is a polynomial in n variables",
    "H_2: The total degree of f is strictly less than n",
    "H_3: There exists at least one point such that f(c) = 0",
    "¬Q: There is NO other distinct point such that f(d) = 0"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    q = None
    
    # Parse witness
    if isinstance(witness, tuple):
        if len(witness) == 3:
            q, n, f = witness
        elif len(witness) == 2:
            if isinstance(witness[0], int):
                n, f = witness
            else:
                domain, f = witness
                f = sp.sympify(f)
                n = len(f.free_symbols)
        else:
            f = witness[0]
            f = sp.sympify(f)
            n = len(f.free_symbols)
    else:
        f = witness
        f = sp.sympify(f)
        n = len(f.free_symbols)

    f = sp.sympify(f)
    if hasattr(f, 'as_expr'):
        f_expr = f.as_expr()
    else:
        f_expr = f

    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    # H1: f is a polynomial
    try:
        poly_f = sp.Poly(f_expr)
        gens = poly_f.gens
        h1 = all(isinstance(gen, sp.Symbol) for gen in gens) and len(gens) <= n
    except Exception:
        h1 = False

    # H2: total degree < n
    try:
        if h1:
            deg = poly_f.total_degree()
            if deg == -sp.oo:
                deg = -1
            h2 = deg < n
    except Exception:
        h2 = False

    # H3 & ¬Q: Root counting
    try:
        if h1:
            k = len(gens)
            
            if q is not None:
                if q < 2:
                    return [False, False, False, False]
                # Check over finite field / ring Z_q
                roots_count = 0
                for pt in itertools.product(range(q), repeat=k):
                    try:
                        val = poly_f(*pt)
                        val_rat = sp.Rational(val)
                        if val_rat.q == 1 and int(val_rat.p) % q == 0:
                            roots_count += 1
                            if roots_count * (q ** (n - k)) > 1:
                                break
                    except Exception:
                        pass
                
                total_roots = roots_count * (q ** (n - k))
                if total_roots >= 1:
                    h3 = True
                if total_roots == 1:
                    neg_q = True
                else:
                    neg_q = False
            else:
                # Check over Reals (infinite field)
                if k == 0:
                    val = float(f_expr)
                    if val == 0:
                        h3 = True
                        if n == 0:
                            neg_q = True
                        else:
                            neg_q = False
                else:
                    z3_vars = {str(g): z3.Real(str(g)) for g in gens}
                    
                    def to_z3(expr):
                        if expr.is_Add:
                            return sum(to_z3(arg) for arg in expr.args)
                        elif expr.is_Mul:
                            res = 1
                            for arg in expr.args:
                                res = res * to_z3(arg)
                            return res
                        elif expr.is_Pow:
                            base = to_z3(expr.args[0])
                            exp = expr.args[1]
                            if exp.is_Integer:
                                return base ** int(exp)
                            else:
                                raise ValueError("Only integer exponents supported")
                        elif expr.is_Symbol:
                            return z3_vars[str(expr)]
                        elif expr.is_Integer:
                            return int(expr)
                        elif expr.is_Rational:
                            return z3.RealVal(f"{expr.p}/{expr.q}")
                        else:
                            return float(expr)

                    solver = z3.Solver()
                    z3_f = to_z3(f_expr)
                    solver.add(z3_f == 0)
                    
                    if solver.check() == z3.sat:
                        h3 = True
                        if n > k:
                            # Dummy variables can take any real value -> infinitely many roots
                            neg_q = False
                        else:
                            model = solver.model()
                            diff_conds = []
                            for g in gens:
                                v = z3_vars[str(g)]
                                m_val = model.eval(v, model_completion=True)
                                diff_conds.append(v != m_val)
                            
                            solver.add(z3.Or(diff_conds))
                            if solver.check() == z3.sat:
                                neg_q = False
                            else:
                                neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]