import sympy

x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = sympy.symbols('x1:11')

def is_zero_mod(expr, xs, m):
    try:
        expr = sympy.expand(expr)
        if not expr.free_symbols.issubset(xs):
            return False
        if expr == 0:
            return True
        poly = sympy.Poly(expr, *xs, domain=sympy.ZZ)
        return all(int(c) % m == 0 for c in poly.coeffs())
    except Exception:
        return False

def conditions(witness):
    try:
        m, n, P, Q = witness
        m = int(m)
        n = int(n)
        if hasattr(P, 'as_expr'): P = P.as_expr()
        if hasattr(Q, 'as_expr'): Q = Q.as_expr()
    except Exception:
        return [False, False]
        
    h1_ok = False
    try:
        if m >= 2 and n >= 1:
            xs = sympy.symbols(f'x1:{n+1}')
            if P.free_symbols.issubset(xs) and Q.free_symbols.issubset(xs):
                sympy.Poly(P, *xs, domain=sympy.ZZ)
                sympy.Poly(Q, *xs, domain=sympy.ZZ)
                
                is_sym = True
                for i in range(n - 1):
                    P_swapped = P.subs({xs[i]: xs[i+1], xs[i+1]: xs[i]})
                    Q_swapped = Q.subs({xs[i]: xs[i+1], xs[i+1]: xs[i]})
                    if not is_zero_mod(P - P_swapped, xs, m) or not is_zero_mod(Q - Q_swapped, xs, m):
                        is_sym = False
                        break
                if is_sym:
                    h1_ok = is_zero_mod(P * Q - 1, xs, m)
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if h1_ok:
            xs = sympy.symbols(f'x1:{n+1}')
            P_const = P.subs({x: 0 for x in xs})
            neg_q_ok = not is_zero_mod(P - P_const, xs, m)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a unit in the ring of symmetric polynomials in n variables over Z/mZ (witnessed by inverse Q)",
    "neg_Q: P is not a constant polynomial"
]

N_HYP = 1
NEG_Q_INDEX = 1