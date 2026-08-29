import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, f, n, a = witness
            elif len(witness) == 3:
                R, f, a = witness
                n = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # H1: R is a commutative ring
        try:
            if hasattr(R, 'is_commutative'):
                h1 = R.is_commutative
            elif hasattr(R, 'is_Ring') and R.is_Ring:
                h1 = True
            elif R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
                h1 = True
            else:
                h1 = True
        except Exception:
            h1 = False
            
        # H2: f(x) is a polynomial over R of degree n
        try:
            if hasattr(f, 'as_expr'):
                f_expr = f.as_expr()
            else:
                f_expr = f
            free = f_expr.free_symbols
            if x in free:
                gen = x
            else:
                gen = list(free)[0] if free else x
                
            f_poly = Poly(f_expr, gen)
            f_coeffs = f_poly.all_coeffs()
            
            f_in_R = True
            for c in f_coeffs:
                if R == sympy.ZZ and not c.is_integer:
                    f_in_R = False
                elif R == sympy.QQ and not c.is_rational:
                    f_in_R = False
                elif R == sympy.RR and not c.is_real:
                    f_in_R = False
                elif hasattr(R, '__contains__') and c not in R:
                    f_in_R = False
                    
            h2 = f_in_R
            if n is not None:
                h2 = h2 and f_poly.degree() == n
        except Exception:
            h2 = False
            
        # neg_Q: The conclusion fails
        try:
            if hasattr(f, 'as_expr'):
                f_expr = f.as_expr()
            else:
                f_expr = f
            free = f_expr.free_symbols
            if x in free:
                gen = x
            else:
                gen = list(free)[0] if free else x
                
            f_shifted = f_expr.subs(gen, gen + a)
            f_shifted_poly = Poly(f_shifted, gen)
            shifted_coeffs = f_shifted_poly.all_coeffs()
            
            all_in_R = True
            for c in shifted_coeffs:
                if R == sympy.ZZ and not c.is_integer:
                    all_in_R = False
                elif R == sympy.QQ and not c.is_rational:
                    all_in_R = False
                elif R == sympy.RR and not c.is_real:
                    all_in_R = False
                elif hasattr(R, '__contains__') and c not in R:
                    all_in_R = False
                    
            neg_q = not all_in_R
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is a polynomial over R of degree n",
    "not Q: The Taylor expansion coefficients are not all in R"
]

N_HYP = 2
NEG_Q_INDEX = 2