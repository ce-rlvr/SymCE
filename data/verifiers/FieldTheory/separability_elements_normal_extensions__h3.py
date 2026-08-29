import sympy as sp

x, y = sp.symbols('x y')

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
        K_str = witness.get('K', 'QQ')
        L_min_poly = sp.sympify(witness.get('L_min_poly', x))
        alpha = sp.sympify(witness.get('alpha', 0))
        f = sp.sympify(witness.get('f', y**2))
    except Exception:
        return [False, False, False]

    h1 = False
    try:
        if K_str == 'QQ':
            if L_min_poly.free_symbols.issubset({x}):
                poly_L = sp.Poly(L_min_poly, x, domain=sp.QQ)
                if poly_L.is_irreducible:
                    deg = poly_L.degree()
                    if deg <= 2:
                        h1 = True
    except Exception:
        h1 = False

    h2 = False
    try:
        if K_str == 'QQ':
            if alpha.free_symbols.issubset({x}):
                h2 = True
    except Exception:
        h2 = False

    neg_q = False
    try:
        if K_str == 'QQ':
            poly_L = sp.Poly(L_min_poly, x, domain=sp.QQ)
            alpha_separable = True
            
            if f == 0:
                splits_distinct = False
            else:
                f_expr = f
                if x in f_expr.free_symbols and poly_L.degree() > 1:
                    f_expr = f_expr.subs(x, y)
                    
                if y in f_expr.free_symbols:
                    f_var = y
                elif len(f_expr.free_symbols) == 1:
                    f_var = list(f_expr.free_symbols)[0]
                else:
                    f_var = y
                    
                if poly_L.degree() == 1:
                    factors = sp.factor_list(f_expr, f_var, domain=sp.QQ)
                else:
                    factors = sp.factor_list(f_expr, f_var, extension=L_min_poly)
                    
                splits_distinct = True
                for fac, mult in factors[1]:
                    if sp.degree(fac, f_var) != 1:
                        splits_distinct = False
                        break
                    if mult != 1:
                        splits_distinct = False
                        break
                        
            conclusion = (alpha_separable == splits_distinct)
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: L/K is a normal extension", "H_2: alpha is an element of L", "not_Q: Conclusion fails"]
N_HYP = 2
NEG_Q_INDEX = 2