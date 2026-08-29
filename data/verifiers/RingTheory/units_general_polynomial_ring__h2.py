import sympy as sp
import math
import itertools
import functools
from sympy import eye, zeros, QQ, ZZ, RR, CC

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Format 1: (f_coeffs, g_coeffs, mod)
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[2], int) and isinstance(witness[0], list):
            f, g, mod = witness
            h1 = True
            
            deg_f = len(f) - 1
            deg_g = len(g) - 1
            deg_h = deg_f + deg_g
            h = [0] * (deg_h + 1)
            
            for i in range(deg_f + 1):
                for j in range(deg_g + 1):
                    h[i+j] = (h[i+j] + f[i] * g[j]) % mod
                    
            h2 = (h[0] == 1)
            for k in range(1, deg_h + 1):
                if h[k] != 0:
                    h2 = False
                    break
                    
            a_0 = f[0] if len(f) > 0 else 0
            higher = f[1:] if len(f) > 1 else []
            
            a_0_is_unit = (math.gcd(a_0, mod) == 1)
            
            all_nil = True
            for c in higher:
                curr = c % mod
                is_nil = False
                for _ in range(mod):
                    if curr == 0:
                        is_nil = True
                        break
                    curr = (curr * c) % mod
                if not is_nil:
                    all_nil = False
                    break
                    
            neg_q = not (a_0_is_unit and all_nil)
            return [bool(h1), bool(h2), bool(neg_q)]

        # Format 2: (n, add_table, mul_table, f_coeffs, g_coeffs)
        if isinstance(witness, tuple) and len(witness) == 5 and isinstance(witness[0], int):
            n, add_table, mul_table, f_coeffs, g_coeffs = witness
            
            if n <= 0:
                return [False, False, False]
                
            def add(x, y): return add_table[x][y]
            def mul(x, y): return mul_table[x][y]
            
            h1 = True
            if len(add_table) != n or any(len(row) != n for row in add_table): h1 = False
            if len(mul_table) != n or any(len(row) != n for row in mul_table): h1 = False
            
            if h1:
                for i in range(n):
                    for j in range(n):
                        if add(i, j) != add(j, i): h1 = False
                        if mul(i, j) != mul(j, i): h1 = False
            
            if h1:
                for i in range(n):
                    for j in range(n):
                        for k in range(n):
                            if add(add(i, j), k) != add(i, add(j, k)): h1 = False
                            if mul(mul(i, j), k) != mul(i, mul(j, k)): h1 = False
                            if mul(i, add(j, k)) != add(mul(i, j), mul(i, k)): h1 = False
            
            zero = None
            if h1:
                for i in range(n):
                    if all(add(i, j) == j for j in range(n)):
                        zero = i
                        break
                if zero is None: h1 = False
                
            if h1:
                for i in range(n):
                    if not any(add(i, j) == zero for j in range(n)):
                        h1 = False
                        break
                        
            one = None
            if h1:
                for i in range(n):
                    if all(mul(i, j) == j for j in range(n)):
                        one = i
                        break
                if one is None: h1 = False
                
            h2 = False
            if h1 and isinstance(f_coeffs, list) and isinstance(g_coeffs, list):
                if len(f_coeffs) > 0 and len(g_coeffs) > 0:
                    deg_f = len(f_coeffs) - 1
                    deg_g = len(g_coeffs) - 1
                    deg_h = deg_f + deg_g
                    h_coeffs = [zero] * (deg_h + 1)
                    
                    for i in range(deg_f + 1):
                        for j in range(deg_g + 1):
                            term = mul(f_coeffs[i], g_coeffs[j])
                            h_coeffs[i+j] = add(h_coeffs[i+j], term)
                            
                    if h_coeffs[0] == one:
                        h2 = True
                        for k in range(1, deg_h + 1):
                            if h_coeffs[k] != zero:
                                h2 = False
                                break
                                
            neg_q = False
            if h1:
                a_0 = f_coeffs[0] if len(f_coeffs) > 0 else zero
                higher_coeffs = f_coeffs[1:] if len(f_coeffs) > 1 else []
                
                a_0_is_unit = any(mul(a_0, b) == one for b in range(n))
                
                all_nilpotent = True
                for a_i in higher_coeffs:
                    is_nil = False
                    curr = a_i
                    for _ in range(n):
                        if curr == zero:
                            is_nil = True
                            break
                        curr = mul(curr, a_i)
                    if not is_nil:
                        all_nilpotent = False
                        break
                        
                neg_q = not (a_0_is_unit and all_nilpotent)
                
            return [bool(h1), bool(h2), bool(neg_q)]

        # Format 3: (domain, f_expr, g_expr)
        if isinstance(witness, tuple) and len(witness) == 3 and hasattr(witness[0], 'is_commutative'):
            domain, f_expr, g_expr = witness
            h1 = getattr(domain, 'is_commutative', False)
            
            x = sp.Symbol('x')
            f_poly = sp.Poly(f_expr, x, domain=domain)
            g_poly = sp.Poly(g_expr, x, domain=domain)
            
            h_poly = f_poly * g_poly
            h2 = (h_poly == sp.Poly(1, x, domain=domain))
            
            coeffs = f_poly.all_coeffs()
            coeffs.reverse()
            if not coeffs:
                coeffs = [domain.zero]
            a_0 = coeffs[0]
            higher = coeffs[1:]
            
            try:
                q, r = domain.div(domain.one, a_0)
                a_0_is_unit = (r == domain.zero)
            except Exception:
                a_0_is_unit = False
                
            all_nil = True
            for c in higher:
                if c != domain.zero:
                    if hasattr(domain, 'is_nilpotent'):
                        if not domain.is_nilpotent(c):
                            all_nil = False
                            break
                    else:
                        all_nil = False
                        break
            neg_q = not (a_0_is_unit and all_nil)
            return [bool(h1), bool(h2), bool(neg_q)]

    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f(x) is a unit in the polynomial ring",
    "¬Q: The constant term a_0 is not a unit in R, or some higher degree coefficient is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2