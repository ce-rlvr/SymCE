import sympy
from sympy import Symbol, Poly, simplify, Rational, Integer, expand, I

x = Symbol('x')
Y = Symbol('Y')

CONDITION_LABELS = [
    "H_1: f is a monic polynomial over R",
    "H_2: alpha in K is a root of f",
    "not Q: alpha is not an element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_in_R(val, d):
    try:
        val_simp = simplify(val)
        val_sym = expand(val_simp).subs(d, Y)
        p = Poly(val_sym, Y)
        for c in p.all_coeffs():
            if not isinstance(c, (int, Integer)):
                return False
        return True
    except Exception:
        return False

def check_in_K(val, d):
    try:
        val_simp = simplify(val)
        val_sym = expand(val_simp).subs(d, Y)
        p = Poly(val_sym, Y)
        for c in p.all_coeffs():
            if not isinstance(c, (int, Integer, Rational)):
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        f = witness['f']
        alpha = witness['alpha']
        d = witness.get('d', None)
        
        if d is None:
            for arg in sympy.preorder_traversal(alpha):
                if isinstance(arg, sympy.Mul) and sympy.I in arg.args:
                    for factor in arg.args:
                        if isinstance(factor, sympy.Pow) and factor.exp == Rational(1, 2):
                            d = sympy.I * factor
                            break
                if d is not None:
                    break
            
            if d is None:
                for arg in sympy.preorder_traversal(alpha):
                    if isinstance(arg, sympy.Pow) and arg.exp == Rational(1, 2):
                        d = arg
                        break
                        
            if d is None and alpha.has(sympy.I):
                d = sympy.I
                
            if d is None:
                d = Symbol('d')
                
        # H_1: f is a monic polynomial over R
        free_syms = f.free_symbols
        if len(free_syms) != 1:
            h1 = False
        else:
            x_sym = list(free_syms)[0]
            p_f = Poly(f, x_sym)
            if not p_f.is_monic:
                h1 = False
            else:
                h1 = True
                for c in p_f.all_coeffs():
                    if not check_in_R(c, d):
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        # H_2: alpha in K is a root of f
        if not check_in_K(alpha, d):
            h2 = False
        else:
            x_sym = list(f.free_symbols)[0]
            if simplify(f.subs(x_sym, alpha)) != 0:
                h2 = False
            else:
                h2 = True
    except Exception:
        h2 = False

    try:
        # neg_Q: alpha is not an element of R
        neg_q = not check_in_R(alpha, d)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]