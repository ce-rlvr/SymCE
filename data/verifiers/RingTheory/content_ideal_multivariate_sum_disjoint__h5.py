import sympy
from sympy import Poly, gcd, sympify, Expr

# Top-level setup
x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: X and Y are disjoint sets of indeterminates over R",
    "H_3: f is a polynomial over X",
    "H_4: g is a polynomial over Y",
    "neg_Q: content of f plus g is not sum of contents"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    h1 = h2 = h3 = h4 = neg_q = False
    
    try:
        if len(witness) == 2:
            f, g = witness
            f = sympify(f)
            g = sympify(g)
            X = tuple(f.free_symbols)
            Y = tuple(g.free_symbols)
        elif len(witness) == 4:
            f, g, X, Y = witness
            f = sympify(f)
            g = sympify(g)
            X = tuple(sympify(var) for var in X)
            Y = tuple(sympify(var) for var in Y)
        else:
            return [False] * 5
            
        # H1: R is a commutative ring
        h1 = True
        for sym in f.free_symbols | g.free_symbols:
            if not sym.is_commutative:
                h1 = False
                break
                
        # H2: X and Y are disjoint sets of indeterminates
        try:
            set_X = set(X)
            set_Y = set(Y)
            h2 = set_X.isdisjoint(set_Y) and all(isinstance(s, Expr) for s in set_X | set_Y)
        except Exception:
            h2 = False
            
        # H3: f is a polynomial over X
        try:
            if X:
                Poly(f, *X)
            else:
                Poly(f)
            h3 = True
        except Exception:
            h3 = False
            
        # H4: g is a polynomial over Y
        try:
            if Y:
                Poly(g, *Y)
            else:
                Poly(g)
            h4 = True
        except Exception:
            h4 = False
            
        # neg_Q: c(f+g) != c(f) + c(g)
        try:
            def get_content(expr, vars):
                if not vars:
                    return expr
                coeffs = Poly(expr, *vars).coeffs()
                res = 0
                for c in coeffs:
                    res = gcd(res, c)
                return res
            
            c_f = get_content(f, X)
            c_g = get_content(g, Y)
            
            XY = tuple(set_X | set_Y)
            c_fg = get_content(f + g, XY)
            
            c_f_plus_c_g = gcd(c_f, c_g)
            
            diff1 = sympy.simplify(c_fg - c_f_plus_c_g)
            diff2 = sympy.simplify(c_fg + c_f_plus_c_g)
            
            neg_q = (diff1 != 0) and (diff2 != 0)
            
        except Exception:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, h4, neg_q]