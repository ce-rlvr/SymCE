import sympy
from sympy import symbols, ZZ, QQ
from sympy.polys.polytools import Poly

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a and b are coprime",
    "¬Q: The intersection of the principal ideals (a) and (b) is not the principal ideal (ab)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False

    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, a, b = witness
                
                # H1: R is a UFD
                try:
                    h1 = bool(getattr(R, 'is_UFD', False))
                except Exception:
                    h1 = False
                
                # H2: a and b are coprime
                try:
                    gcd_val = R.gcd(a, b)
                    if hasattr(R, 'is_unit'):
                        h2 = bool(R.is_unit(gcd_val))
                    else:
                        try:
                            R.exquo(R.one, gcd_val)
                            h2 = True
                        except Exception:
                            h2 = (gcd_val == R.one or gcd_val == -R.one)
                except Exception:
                    h2 = False

                # neg_Q: (a) \cap (b) != (ab)
                try:
                    lcm_val = R.lcm(a, b)
                    ab = R.mul(a, b)
                    if lcm_val == R.zero and ab == R.zero:
                        ideals_equal = True
                    elif lcm_val == R.zero or ab == R.zero:
                        ideals_equal = False
                    else:
                        try:
                            R.exquo(ab, lcm_val)
                            R.exquo(lcm_val, ab)
                            ideals_equal = True
                        except Exception:
                            ideals_equal = False
                    neg_q = not ideals_equal
                except Exception:
                    neg_q = False

                return [h1, h2, neg_q]
            
            elif len(witness) == 2:
                a, b = witness
                
                try:
                    a_sym = sympy.sympify(a)
                    b_sym = sympy.sympify(b)
                    
                    poly_a = Poly(a_sym)
                    poly_b = Poly(b_sym)
                    domain = poly_a.domain.unify(poly_b.domain)
                    
                    # H1: R is a UFD
                    h1 = bool(getattr(domain, 'is_UFD', False))
                    
                    a_dom = domain.from_sympy(a_sym)
                    b_dom = domain.from_sympy(b_sym)
                    
                    # H2: a and b are coprime
                    try:
                        gcd_val = domain.gcd(a_dom, b_dom)
                        if hasattr(domain, 'is_unit'):
                            h2 = bool(domain.is_unit(gcd_val))
                        else:
                            try:
                                domain.exquo(domain.one, gcd_val)
                                h2 = True
                            except Exception:
                                h2 = (gcd_val == domain.one or gcd_val == -domain.one)
                    except Exception:
                        h2 = False
                        
                    # neg_Q: (a) \cap (b) != (ab)
                    try:
                        lcm_val = domain.lcm(a_dom, b_dom)
                        ab = domain.mul(a_dom, b_dom)
                        
                        if lcm_val == domain.zero and ab == domain.zero:
                            ideals_equal = True
                        elif lcm_val == domain.zero or ab == domain.zero:
                            ideals_equal = False
                        else:
                            try:
                                domain.exquo(ab, lcm_val)
                                domain.exquo(lcm_val, ab)
                                ideals_equal = True
                            except Exception:
                                ideals_equal = False
                                
                        neg_q = not ideals_equal
                    except Exception:
                        neg_q = False

                    return [h1, h2, neg_q]
                except Exception:
                    pass
    except Exception:
        pass

    return [False, False, False]