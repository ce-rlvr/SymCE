import sympy
from sympy import Poly, div
import itertools

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
                domain = 'ZZ'
            elif len(witness) == 3:
                f, g, domain = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(domain, str):
            if domain in ('ZZ', 'QQ'):
                pass
            elif domain.startswith('ZZ_'):
                domain = int(domain[3:])
            elif domain.startswith('Z'):
                domain = int(domain[1:])
                    
        try:
            if domain == 'ZZ':
                f_poly = Poly(f, x, domain='ZZ')
                g_poly = Poly(g, x, domain='ZZ')
            elif isinstance(domain, int):
                f_poly = Poly(f, x, domain=f'ZZ_{domain}')
                g_poly = Poly(g, x, domain=f'ZZ_{domain}')
            elif domain == 'QQ':
                f_poly = Poly(f, x, domain='QQ')
                g_poly = Poly(g, x, domain='QQ')
            else:
                f_poly = Poly(f, x)
                g_poly = Poly(g, x)
            h1 = True
        except Exception:
            h1 = False
            
        try:
            h2 = not g_poly.is_zero
        except Exception:
            h2 = False
            
        neg_q = False
        try:
            if domain == 'ZZ':
                q, r = div(f, g, domain='QQ')
                q_poly = Poly(q, x)
                r_poly = Poly(r, x)
                
                def is_int_poly(p):
                    return all(c.is_integer for c in p.coeffs())
                    
                if not (is_int_poly(q_poly) and is_int_poly(r_poly)):
                    neg_q = True
                else:
                    neg_q = False
                    
            elif isinstance(domain, int):
                n = domain
                deg_g = g_poly.degree()
                if deg_g == sympy.S.NegativeInfinity:
                    deg_g = -1
                else:
                    deg_g = int(deg_g)
                    
                deg_f = f_poly.degree()
                if deg_f == sympy.S.NegativeInfinity:
                    deg_f = -1
                else:
                    deg_f = int(deg_f)
                    
                max_deg_q = max(0, deg_f - deg_g) + 1
                
                def gen_polys(max_deg):
                    if max_deg < 0:
                        yield Poly(0, x, domain=f'ZZ_{n}')
                        return
                    for coeffs in itertools.product(range(n), repeat=max_deg + 1):
                        yield Poly(list(coeffs), x, domain=f'ZZ_{n}')
                        
                solutions = 0
                for q in gen_polys(max_deg_q):
                    r = f_poly - q * g_poly
                    if r.is_zero or int(r.degree()) < deg_g:
                        solutions += 1
                        if solutions > 1:
                            neg_q = True
                            break
                            
                if solutions == 0:
                    neg_q = True
                elif solutions == 1 and not neg_q:
                    for q0 in gen_polys(0):
                        if not q0.is_zero and (q0 * g_poly).is_zero:
                            neg_q = True
                            break
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: f and g are polynomials", "H_2: g is a non-zero polynomial", "neg_Q: The division algorithm fails"]
N_HYP = 2
NEG_Q_INDEX = 2