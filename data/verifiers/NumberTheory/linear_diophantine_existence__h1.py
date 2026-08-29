import sympy
from sympy import gcd, simplify, Rational
import math
from sympy.abc import x, y, z, t
from sympy import sqrt, pi, I, exp, sin, cos

def _is_int(val):
    if isinstance(val, int):
        return True
    if hasattr(val, 'is_Rational') and val.is_Rational:
        return val.q == 1
    if hasattr(val, 'is_number') and val.is_number:
        try:
            return float(val).is_integer()
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        a, b, c = witness
    except Exception:
        return [False, False]
        
    # H1: a and b are not both zero
    try:
        h1 = not (simplify(a) == 0 and simplify(b) == 0)
    except Exception:
        h1 = False
        
    # Conclusion: ax + by = c has integer solutions iff gcd(a, b) divides c
    try:
        g = gcd(a, b)
        if simplify(g) == 0:
            gcd_divides = (simplify(c) == 0)
        else:
            quot = simplify(c / g)
            gcd_divides = _is_int(quot)
            
        has_sol = False
        is_rat = False
        try:
            A_rat = Rational(a)
            B_rat = Rational(b)
            C_rat = Rational(c)
            is_rat = True
        except Exception:
            pass
            
        if is_rat:
            try:
                da, db, dc = A_rat.q, B_rat.q, C_rat.q
                lcm_d = math.lcm(da, math.lcm(db, dc))
                A_int = int(A_rat.p * (lcm_d / A_rat.q))
                B_int = int(B_rat.p * (lcm_d / B_rat.q))
                C_int = int(C_rat.p * (lcm_d / C_rat.q))
                g_int = math.gcd(A_int, B_int)
                if g_int == 0:
                    has_sol = (C_int == 0)
                else:
                    has_sol = (C_int % g_int == 0)
            except Exception:
                pass
        else:
            try:
                a_expr = simplify(a)
                b_expr = simplify(b)
                c_expr = simplify(c)
                
                terms_a = a_expr.as_coefficients_dict()
                terms_b = b_expr.as_coefficients_dict()
                terms_c = c_expr.as_coefficients_dict()
                
                all_bases = set(terms_a.keys()) | set(terms_b.keys()) | set(terms_c.keys())
                
                parsed_eqs = []
                for base in all_bases:
                    ca = terms_a.get(base, 0)
                    cb = terms_b.get(base, 0)
                    cc = terms_c.get(base, 0)
                    
                    A_r = Rational(ca)
                    B_r = Rational(cb)
                    C_r = Rational(cc)
                    
                    da, db, dc = A_r.q, B_r.q, C_r.q
                    lcm_d = math.lcm(da, math.lcm(db, dc))
                    A_i = int(A_r.p * (lcm_d / A_r.q))
                    B_i = int(B_r.p * (lcm_d / B_r.q))
                    C_i = int(C_r.p * (lcm_d / C_r.q))
                    
                    if A_i != 0 or B_i != 0 or C_i != 0:
                        parsed_eqs.append((A_i, B_i, C_i))
                
                if not parsed_eqs:
                    has_sol = True
                else:
                    x_sym, y_sym = sympy.symbols('x_sym y_sym')
                    sympy_eqs = [A*x_sym + B*y_sym - C for A, B, C in parsed_eqs]
                    sol = sympy.linsolve(sympy_eqs, (x_sym, y_sym))
                    
                    if not sol:
                        has_sol = False
                    else:
                        sol_tuple = list(sol)[0]
                        x_sol, y_sol = sol_tuple
                        
                        if x_sol.is_number and y_sol.is_number:
                            has_sol = _is_int(x_sol) and _is_int(y_sol)
                        else:
                            A_first, B_first, C_first = parsed_eqs[0]
                            g_int = math.gcd(A_first, B_first)
                            if g_int == 0:
                                has_sol = (C_first == 0)
                            else:
                                has_sol = (C_first % g_int == 0)
            except Exception:
                found = False
                for x_val in range(-100, 101):
                    for y_val in range(-100, 101):
                        diff = a * x_val + b * y_val - c
                        if diff == 0 or sympy.expand(diff) == 0:
                            found = True
                            break
                    if found:
                        break
                has_sol = found

        concl = (has_sol == gcd_divides)
        neg_q = not concl
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are not both zero",
    "¬Q: The conclusion fails (ax + by = c has integer solutions iff gcd(a, b) divides c)"
]

N_HYP = 1
NEG_Q_INDEX = 1