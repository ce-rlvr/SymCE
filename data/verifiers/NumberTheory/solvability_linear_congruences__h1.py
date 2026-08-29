import sympy as sp
import math

CONDITION_LABELS = [
    "H_1: m > 0",
    "H_2: d = gcd(a, m)",
    "¬Q: The equivalence (ax ≡ b mod m has an integer solution iff d divides b) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_int(val):
    if isinstance(val, (int, sp.Integer)):
        return True
    if hasattr(val, 'is_integer'):
        prop = val.is_integer
        if callable(prop):
            try:
                return prop()
            except Exception:
                return False
        return bool(prop)
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            m = witness['m']
            d = witness.get('d', sp.gcd(a, m))
        elif isinstance(witness, (tuple, list)):
            a = witness[0]
            b = witness[1]
            m = witness[2]
            d = witness[3] if len(witness) > 3 else sp.gcd(a, m)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: m > 0
    try:
        res = m > 0
        if isinstance(res, bool):
            h1 = res
        else:
            h1 = bool(res)
    except Exception:
        h1 = False

    # H2: d = gcd(a, m)
    try:
        h2 = bool(d == sp.gcd(a, m))
    except Exception:
        h2 = False

    # P_sol: exists integer x such that ax ≡ b (mod m)
    try:
        P_sol = False
        
        if is_int(a) and is_int(b) and is_int(m):
            P_sol = (int(b) % math.gcd(int(a), int(m))) == 0
        else:
            # Try polynomial / symbolic approach
            x_sol, k_sol = sp.symbols('x_sol k_sol', integer=True)
            expr = a * x_sol - m * k_sol - b
            if hasattr(expr, 'free_symbols'):
                free = expr.free_symbols - {x_sol, k_sol}
                if free:
                    poly = sp.Poly(expr, *free)
                    coeffs = poly.coeffs()
                    sol = sp.linsolve(coeffs, (x_sol, k_sol))
                    if sol:
                        for s in sol:
                            x_val, k_val = s
                            if is_int(x_val) and is_int(k_val):
                                P_sol = True
                                break
                            if isinstance(x_val, sp.Rational) and x_val.q == 1 and \
                               isinstance(k_val, sp.Rational) and k_val.q == 1:
                                P_sol = True
                                break
            
            # Fallback to brute-force search for small integers (handles irrationals/floats)
            if not P_sol:
                has_syms = False
                for var in (a, b, m):
                    if hasattr(var, 'free_symbols') and var.free_symbols:
                        has_syms = True
                        break
                
                limit = 100 if has_syms else 1000
                for x_val in range(-limit, limit + 1):
                    if m == 0:
                        if sp.simplify(a * x_val - b) == 0:
                            P_sol = True
                            break
                        continue
                    
                    num = a * x_val - b
                    
                    # Fast float check to avoid slow simplify
                    if not has_syms:
                        try:
                            k_f = float(num) / float(m)
                            if abs(k_f - round(k_f)) > 1e-6:
                                continue
                        except Exception:
                            pass
                            
                    k_val = sp.simplify(num / m)
                    if is_int(k_val):
                        P_sol = True
                        break
                    if isinstance(k_val, sp.Rational) and k_val.q == 1:
                        P_sol = True
                        break
                    if hasattr(k_val, 'evalf'):
                        try:
                            kf = float(k_val.evalf())
                            if abs(kf - round(kf)) < 1e-12:
                                if sp.simplify(num - m * round(kf)) == 0:
                                    P_sol = True
                                    break
                        except Exception:
                            pass
    except Exception:
        P_sol = False

    # Q_div: d divides b
    try:
        Q_div = False
        if d == 0:
            Q_div = (b == 0)
        elif is_int(b) and is_int(d):
            Q_div = (int(b) % int(d) == 0)
        else:
            ratio = sp.simplify(b / d)
            if is_int(ratio):
                Q_div = True
            elif isinstance(ratio, sp.Rational) and ratio.q == 1:
                Q_div = True
            elif hasattr(ratio, 'evalf'):
                try:
                    rf = float(ratio.evalf())
                    if abs(rf - round(rf)) < 1e-12:
                        if sp.simplify(b - d * round(rf)) == 0:
                            Q_div = True
                except Exception:
                    pass
    except Exception:
        Q_div = False

    neg_q = (P_sol != Q_div)

    return [h1, h2, neg_q]