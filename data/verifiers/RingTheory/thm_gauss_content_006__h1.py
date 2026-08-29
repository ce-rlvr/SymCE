import sympy

X = sympy.Symbol('X')
Y = sympy.Symbol('Y')

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, x_sym, y_sym = witness
            else:
                f = witness[0]
                syms = sorted(f.free_symbols, key=lambda s: s.name)
                x_sym, y_sym = (syms[0], syms[1]) if len(syms) >= 2 else (X, Y)
        else:
            f = witness
            if hasattr(f, 'free_symbols'):
                syms = sorted(f.free_symbols, key=lambda s: s.name)
                x_sym, y_sym = (syms[0], syms[1]) if len(syms) >= 2 else (X, Y)
            else:
                x_sym, y_sym = X, Y
                
        if hasattr(f, 'as_expr'):
            f = f.as_expr()
            
        p_f = sympy.Poly(f, (x_sym, y_sym))
        h1_ok = not p_f.is_zero
        
        h2_ok = True
        
        p_Y = sympy.Poly(f, y_sym)
        c_Y = sympy.gcd_list(p_Y.coeffs())
        
        p_cY = sympy.Poly(c_Y, x_sym)
        cont_cY = sympy.gcd_list(p_cY.coeffs())
        
        cont_f = sympy.gcd_list(p_f.coeffs())
        
        try:
            diff = sympy.simplify(cont_cY - cont_f)
            diff_plus = sympy.simplify(cont_cY + cont_f)
            is_diff_zero = (diff == 0) or (diff_plus == 0)
        except Exception:
            is_diff_zero = False
            
        try:
            ratio = sympy.simplify(cont_cY / cont_f)
            is_ratio_unit = (ratio == 1) or (ratio == -1)
        except Exception:
            is_ratio_unit = False
            
        is_equal = (cont_cY == cont_f) or is_diff_zero or is_ratio_unit
        neg_q_ok = not is_equal
        
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: f is a non-zero polynomial", "H_2: c_Y is the content of f viewed as a polynomial in Y", "not Q: The content of c_Y is not equal to the total content of f"]
N_HYP = 2
NEG_Q_INDEX = 2