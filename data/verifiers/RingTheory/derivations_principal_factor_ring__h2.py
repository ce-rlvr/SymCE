import sympy as sp

# Top-level setup for potential witness expressions
x, y, z, t = sp.symbols('x y z t')

def conditions(witness):
    try:
        f_expr = sp.sympify(witness)
        
        if isinstance(witness, sp.Poly):
            X = list(witness.free_symbols)
            f_expr = witness.as_expr()
        else:
            X = list(f_expr.free_symbols)
            
        if not X:
            X = [sp.Symbol('x')]
            
        try:
            poly = sp.Poly(f_expr, *X)
            domain = poly.domain
            h1 = (domain.char == 0)
            h2 = True
        except Exception:
            return [False, False, False]
            
        if f_expr.is_zero:
            lhs = False
            rhs = False
        elif poly.degree() == 0:
            lhs = True
            rhs = True
        else:
            if len(X) == 1:
                try:
                    var = X[0]
                    df = sp.diff(f_expr, var)
                    g = sp.gcd(f_expr, df)
                    g_poly = sp.Poly(g, var)
                    lhs = (g_poly.degree() == 0)
                except Exception:
                    lhs = False
            else:
                lhs = False
                
            try:
                sqf = sp.sqf_list(f_expr)
                rhs = all(mult == 1 for factor, mult in sqf[1])
            except Exception:
                rhs = False
                
        neg_q = (lhs != rhs)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "H_2: R is the factor ring",
    "not Q: Derivation module is zero iff no repeated roots"
]

N_HYP = 2
NEG_Q_INDEX = 2