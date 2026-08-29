import sympy
from sympy import Poly, resultant, factor, isprime
from sympy.abc import x, y, t

# Standard bindings
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    witness can be a dict with keys: 'p', 'x', 'y', 'E_poly', 'f_poly'
    representing K = GF(p)(y), E = K[x]/(E_poly), and f(x) in K[x].
    Alternatively, witness can be a tuple (E_poly, f_poly) of sympy.Poly objects.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            x_var = witness.get('x', x)
            y_var = witness.get('y', y)
            E_expr = witness.get('E_poly')
            f_expr = witness.get('f_poly')
            
            if None in (p, E_expr, f_expr):
                return [False, False, False]
                
            h1 = isprime(p)
            
            f_poly_x = Poly(f_expr, x_var)
            if f_poly_x.degree() <= 0:
                h2 = False
            else:
                f_diff = f_expr.diff(x_var)
                res_f = resultant(f_expr, f_diff, x_var)
                try:
                    res_f_poly = Poly(res_f, y_var, domain=sympy.GF(p))
                    h2 = not res_f_poly.is_zero
                except Exception:
                    h2 = False
                    
            E_poly_x = Poly(E_expr, x_var)
            if E_poly_x.degree() <= 0:
                neg_q = False
            else:
                E_diff = E_expr.diff(x_var)
                res_E = resultant(E_expr, E_diff, x_var)
                try:
                    res_E_poly = Poly(res_E, y_var, domain=sympy.GF(p))
                    is_insep = res_E_poly.is_zero
                except Exception:
                    is_insep = False
                    
                coeffs = E_poly_x.all_coeffs()
                is_eisenstein = False
                if len(coeffs) > 1:
                    try:
                        a_n_poly = Poly(coeffs[0], y_var, domain=sympy.GF(p))
                        if a_n_poly.nth(0) != 0:
                            div_by_y = True
                            for c in coeffs[1:]:
                                c_poly = Poly(c, y_var, domain=sympy.GF(p))
                                if c_poly.nth(0) != 0:
                                    div_by_y = False
                                    break
                            if div_by_y:
                                a_0_poly = Poly(coeffs[-1], y_var, domain=sympy.GF(p))
                                y_poly = Poly(y_var, y_var, domain=sympy.GF(p))
                                rem = a_0_poly % (y_poly**2)
                                if not rem.is_zero:
                                    is_eisenstein = True
                    except Exception:
                        pass
                        
                is_irred = is_eisenstein
                if not is_irred:
                    try:
                        factored = factor(E_expr, modulus=p)
                        if factored == E_expr:
                            is_irred = True
                    except Exception:
                        pass
                        
                neg_q = is_irred and is_insep
                
            return [bool(h1), bool(h2), bool(neg_q)]
            
        elif isinstance(witness, tuple) and len(witness) == 2:
            E_poly, f_poly = witness
            
            if not (hasattr(E_poly, 'domain') and hasattr(f_poly, 'domain')):
                return [False, False, False]
                
            domain = E_poly.domain
            h1 = domain.is_Field and f_poly.domain == domain
            
            f_diff = f_poly.diff()
            g_f = f_poly.gcd(f_diff)
            h2 = g_f.degree() == 0 and f_poly.degree() > 0
            
            try:
                is_irred = E_poly.is_irreducible
            except Exception:
                is_irred = True
                
            E_diff = E_poly.diff()
            g_E = E_poly.gcd(E_diff)
            is_insep = g_E.degree() > 0 and E_poly.degree() > 0
            
            neg_q = is_irred and is_insep
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a separable polynomial",
    "not Q: E over K is not a separable extension"
]

N_HYP = 2
NEG_Q_INDEX = 2