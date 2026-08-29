import sympy as sp
import math

# Top-level setup
S = sp.sqrt(-5)
x = sp.Symbol('x')

def get_ab(expr):
    expr = sp.sympify(expr)
    expr = sp.radsimp(expr)
    expr = sp.expand(expr)
    a = expr.subs(S, 0)
    b = (expr - a) / S
    b = sp.simplify(b)
    if not (a.is_Rational and b.is_Rational):
        raise ValueError("Not in Q(sqrt(-5))")
    return a, b

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            coeffs = witness
        else:
            poly = sp.Poly(witness, x)
            coeffs = poly.all_coeffs()
    except Exception:
        return [False, False]
    
    try:
        if len(coeffs) == 0:
            h1 = False
        else:
            parsed_coeffs = [get_ab(c) for c in coeffs]
            h1 = any(a != 0 or b != 0 for a, b in parsed_coeffs)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            denoms = []
            for a, b in parsed_coeffs:
                denoms.append(sp.fraction(a)[1])
                denoms.append(sp.fraction(b)[1])
            
            D = 1
            for d in denoms:
                D = sp.lcm(D, d)
            
            int_coeffs = []
            for a, b in parsed_coeffs:
                u = int(a * D)
                v = int(b * D)
                int_coeffs.append((u, v))
            
            g = 0
            for i in range(len(int_coeffs)):
                for j in range(len(int_coeffs)):
                    ui, vi = int_coeffs[i]
                    uj, vj = int_coeffs[j]
                    u = ui*uj + 5*vi*vj
                    v = vi*uj - ui*vj
                    g = math.gcd(g, u)
                    g = math.gcd(g, v)
            
            def is_norm_principal(N):
                if N < 0: return False
                if N == 0: return True
                max_y = int((N / 5)**0.5)
                for y in range(max_y + 1):
                    rem = N - 5 * y**2
                    if rem < 0: continue
                    x_val = int(rem**0.5)
                    if x_val * x_val == rem:
                        return True
                return False
            
            neg_q = not is_norm_principal(g)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: f is non-zero", "¬Q: no fractional content factorization"]
N_HYP = 1
NEG_Q_INDEX = 1