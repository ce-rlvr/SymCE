import sympy as sp
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x')
x0, x1, x2, x3, x4 = sp.symbols('x0 x1 x2 x3 x4')

def conditions(witness):
    try:
        f = witness.get('f')
        roots = witness.get('roots')
        R = witness.get('R')
        x_var = witness.get('x', x)
        vars_list = witness.get('vars', [x0, x1])
        
        if f is None or roots is None or R is None:
            return [False, False, False, False]
            
        # H1: f is a polynomial over QQ
        try:
            f_poly = sp.Poly(f, x_var)
            h1 = all((c.is_rational == True) for c in f_poly.coeffs())
        except Exception:
            h1 = False
            
        # H2: roots are the roots of f
        try:
            h2_1 = len(roots) == f_poly.degree()
            h2_2 = all(sp.simplify(f.subs(x_var, r)) == 0 for r in roots)
            h2 = h2_1 and h2_2
        except Exception:
            h2 = False
            
        # H3: R is a rational function over QQ
        def is_rational_func(expr):
            if isinstance(expr, sp.Symbol):
                return True
            if isinstance(expr, sp.Rational):
                return True
            if isinstance(expr, (sp.Add, sp.Mul)):
                return all(is_rational_func(arg) for arg in expr.args)
            if isinstance(expr, sp.Pow):
                return is_rational_func(expr.base) and isinstance(expr.exp, sp.Integer)
            return False
            
        try:
            h3 = isinstance(R, sp.Expr) and all(s in vars_list for s in R.free_symbols) and is_rational_func(R)
        except Exception:
            h3 = False
            
        # Evaluate R for all permutations of roots to check Galois invariance
        try:
            vals = []
            for p in itertools.permutations(roots):
                sub_dict = {vars_list[i]: p[i] for i in range(min(len(vars_list), len(p)))}
                val = R.subs(sub_dict)
                vals.append(val)
                
            first_val = vals[0]
            
            def is_eq(v1, v2):
                if v1 is sp.nan and v2 is sp.nan:
                    return True
                if v1 == v2:
                    return True
                try:
                    diff = sp.simplify(v1 - v2)
                    return diff == 0
                except Exception:
                    return False
                    
            is_fixed_Sn = all(is_eq(v, first_val) for v in vals)
            
            if first_val in (sp.zoo, sp.nan):
                in_QQ = False
            else:
                simp_val = sp.simplify(first_val)
                in_QQ = (simp_val.is_rational == True)
                
            # The conclusion states: fixed by Gal(E/F) iff in F.
            # If the value is fixed by S_n, it is fixed by Gal(E/F) (since Gal is a subgroup of S_n).
            # If it is fixed by Gal(E/F) but does NOT belong to F, the conclusion fails.
            neg_Q = is_fixed_Sn and not in_QQ
        except Exception:
            neg_Q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over QQ",
    "H_2: roots are the roots of f(x)",
    "H_3: R is a rational function over QQ",
    "¬Q: The value of R is fixed by Gal(E/QQ) but does not belong to QQ"
]

N_HYP = 3
NEG_Q_INDEX = 3