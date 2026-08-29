import sympy
import math

x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            p = witness.get('p')
            u = witness.get('u')
        else:
            a, b, p, u = witness
    except Exception:
        return [False] * 5

    try:
        u_prime = sympy.diff(u, x)
    except Exception:
        u_prime = None

    # H1: I = (a, b) is a bounded open interval in R
    try:
        a_val = float(a)
        b_val = float(b)
        H1 = a_val < b_val
    except Exception:
        H1 = False

    # H2: u is absolutely continuous on [a, b]
    H2 = False
    if H1 and u_prime is not None:
        try:
            dx = (b_val - a_val) / 2000.0
            total = 0.0
            ua = float(u.subs(x, a_val))
            H2 = True
            for i in range(2000):
                xi = a_val + (i + 0.5) * dx
                try:
                    val = float(u_prime.subs(x, xi))
                    total += val * dx
                except Exception:
                    pass
                
                if i % 200 == 0:
                    x_curr = a_val + (i + 1) * dx
                    try:
                        u_curr = float(u.subs(x, x_curr))
                        tol = 0.15 * max(1.0, abs(u_curr - ua)) + 0.15
                        if abs((u_curr - ua) - total) > tol:
                            H2 = False
                            break
                    except Exception:
                        pass
            if H2:
                try:
                    ub = float(u.subs(x, b_val))
                    tol = 0.15 * max(1.0, abs(ub - ua)) + 0.15
                    if abs((ub - ua) - total) > tol:
                        H2 = False
                except Exception:
                    H2 = False
        except Exception:
            H2 = False

    # H3: u(a) = u(b) = 0
    H3 = False
    if H1:
        try:
            ua = float(u.subs(x, a_val))
            ub = float(u.subs(x, b_val))
            H3 = abs(ua) < 1e-7 and abs(ub) < 1e-7
        except Exception:
            H3 = False

    # H4: u' in L^p(I)
    H4 = False
    if H1 and u_prime is not None:
        try:
            p_val = float(p)
            dx = (b_val - a_val) / 2000.0
            total = 0.0
            H4 = True
            zero_count = 0
            for i in range(2000):
                xi = a_val + (i + 0.5) * dx
                try:
                    val = float(u_prime.subs(x, xi))
                    if val == 0 and p_val < 0:
                        zero_count += 1
                        continue
                    term = abs(val)**p_val
                    total += term * dx
                except Exception:
                    zero_count += 1
            
            if zero_count > 10:
                H4 = False
            elif H4:
                H4 = math.isfinite(total)
        except Exception:
            H4 = False

    # neg_Q: \int_a^b |u(x)|^p dx > (b-a)^p \int_a^b |u'(x)|^p dx
    neg_Q = False
    if H1 and u_prime is not None:
        try:
            p_val = float(p)
            dx = (b_val - a_val) / 2000.0
            int_u = 0.0
            int_du = 0.0
            zero_count_u = 0
            zero_count_du = 0
            for i in range(2000):
                xi = a_val + (i + 0.5) * dx
                
                try:
                    u_val = float(u.subs(x, xi))
                    if u_val == 0 and p_val < 0:
                        zero_count_u += 1
                    else:
                        int_u += (abs(u_val)**p_val) * dx
                except Exception:
                    zero_count_u += 1
                
                try:
                    du_val = float(u_prime.subs(x, xi))
                    if du_val == 0 and p_val < 0:
                        zero_count_du += 1
                    else:
                        int_du += (abs(du_val)**p_val) * dx
                except Exception:
                    zero_count_du += 1
                    
            if zero_count_du > 10:
                neg_Q = False
            elif zero_count_u > 10:
                neg_Q = True
            else:
                rhs = ((b_val - a_val)**p_val) * int_du
                neg_Q = int_u > rhs + 1e-5
        except Exception:
            neg_Q = False

    return [H1, H2, H3, H4, neg_Q]

CONDITION_LABELS = ["H_1: I is a bounded open interval in R", "H_2: u is absolutely continuous", "H_3: u(a) = u(b) = 0", "H_4: u prime in L^p", "¬Q: integral of |u|^p > (b-a)^p * integral of |u prime|^p"]

N_HYP = 4
NEG_Q_INDEX = 4