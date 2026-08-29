import sympy as sp

x, y, z = sp.symbols('x y z')

CONDITION_LABELS = [
    "H_1: f(x) is a non-zero polynomial over R",
    "H_2: k >= 1 is an integer",
    "¬Q: The content of f(x^k) is not associate to the content of f(x) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, k = witness
                f = sp.sympify(f)
                free = f.free_symbols
                if len(free) == 1:
                    var_x = list(free)[0]
                elif len(free) == 0:
                    var_x = sp.Symbol('x')
                else:
                    var_x = sp.Symbol('x')
                    if var_x not in free:
                        var_x = list(free)[0]
            elif len(witness) == 3:
                f, var_x, k = witness
                f = sp.sympify(f)
                if isinstance(var_x, str):
                    var_x = sp.Symbol(var_x)
                else:
                    var_x = sp.sympify(var_x)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        k = sp.sympify(k)
        
        try:
            poly_f = sp.Poly(f, var_x)
            is_poly = True
        except Exception:
            is_poly = False
            
        h1 = is_poly and (f != 0)
        
        try:
            h2 = k.is_integer and k >= 1
            if h2:
                k = int(k)
        except Exception:
            h2 = False
            
        try:
            c_f = poly_f.content()
            
            f_sub = f.subs(var_x, var_x**k)
            poly_f_sub = sp.Poly(f_sub, var_x)
            c_f_sub = poly_f_sub.content()
            
            f_pow = f**k
            poly_f_pow = sp.Poly(f_pow, var_x)
            c_f_pow = poly_f_pow.content()
            
            def are_associate(a, b):
                if a == b or a == -b:
                    return True
                try:
                    ratio = sp.simplify(a / b)
                    if ratio == 1 or ratio == -1:
                        return True
                except Exception:
                    pass
                return False

            assoc_sub = are_associate(c_f_sub, c_f)
            assoc_pow = are_associate(c_f_pow, c_f)
            
            neg_q = not assoc_sub or not assoc_pow
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]