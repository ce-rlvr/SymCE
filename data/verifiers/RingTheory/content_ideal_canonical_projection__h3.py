import sympy
from sympy.abc import x, y, z, t

def conditions(witness):
    try:
        vars, I_gens, f_coeffs = witness
        vars = [sympy.sympify(v) for v in vars]
        I_gens = [sympy.sympify(g) for g in I_gens]
        f_coeffs = [sympy.sympify(c) for c in f_coeffs]
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = isinstance(vars, (list, tuple)) and all(isinstance(v, sympy.Symbol) for v in vars)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(I_gens, (list, tuple)) and all(
            isinstance(g, sympy.Expr) and g.free_symbols.issubset(set(vars)) and (not vars or g.is_polynomial(*vars))
            for g in I_gens
        )
    except Exception:
        h2 = False
        
    try:
        h3 = isinstance(f_coeffs, (list, tuple)) and len(f_coeffs) > 0 and all(
            isinstance(c, sympy.Expr) and c.free_symbols.issubset(set(vars)) and (not vars or c.is_polynomial(*vars))
            for c in f_coeffs
        )
    except Exception:
        h3 = False
        
    neg_q = False
    try:
        if h1 and h2 and h3:
            cf = f_coeffs[0]
            for coeff in f_coeffs[1:]:
                cf = sympy.gcd(cf, coeff)
            
            ideal_gens = list(f_coeffs) + list(I_gens)
            
            if not vars:
                if all(g.is_integer for g in ideal_gens) and all(c.is_integer for c in f_coeffs):
                    igcd = ideal_gens[0]
                    for g in ideal_gens[1:]:
                        igcd = sympy.gcd(igcd, g)
                    if igcd == 0:
                        neg_q = (cf != 0)
                    else:
                        neg_q = not sympy.simplify(cf / igcd).is_integer
                else:
                    is_zero_ideal = all(g == 0 for g in ideal_gens)
                    if is_zero_ideal:
                        neg_q = (cf != 0)
                    else:
                        neg_q = False
            else:
                try:
                    gb_zz = sympy.groebner(ideal_gens, *vars, domain='ZZ')
                    rem_zz = sympy.reduced(cf, gb_zz, *vars, domain='ZZ')[1]
                    if rem_zz != 0:
                        neg_q = True
                except Exception:
                    pass
                
                if not neg_q:
                    try:
                        gb_qq = sympy.groebner(ideal_gens, *vars, domain='QQ')
                        rem_qq = sympy.reduced(cf, gb_qq, *vars, domain='QQ')[1]
                        if rem_qq != 0:
                            neg_q = True
                    except Exception:
                        pass
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "H_3: f is a polynomial over R",
    "¬Q: The content ideal of the projected polynomial is not equal to the projected content ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3