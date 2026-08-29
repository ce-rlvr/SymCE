import z3
import math
import sympy
from sympy import Rational, Integer, Poly
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects needed for this domain)

def is_primitive(f_coeffs, m):
    g = m
    for c in f_coeffs:
        g = math.gcd(g, c)
    return g == 1

def check_irreducible(f_coeffs, m):
    f_coeffs = list(f_coeffs)
    while f_coeffs and f_coeffs[0] % m == 0:
        f_coeffs.pop(0)
    if len(f_coeffs) <= 1:
        return False
        
    d = len(f_coeffs) - 1
    max_deg = d + 2
    
    solver = z3.Solver()
    sid = id(solver)
    
    g = [z3.Int(f'g_{sid}_{i}') for i in range(max_deg + 1)]
    h = [z3.Int(f'h_{sid}_{i}') for i in range(max_deg + 1)]
    
    for i in range(max_deg + 1):
        solver.add(g[i] >= 0, g[i] < m)
        solver.add(h[i] >= 0, h[i] < m)
        
    for k in range(2 * max_deg + 1):
        coeff_sum = 0
        for i in range(max_deg + 1):
            j = k - i
            if 0 <= j <= max_deg:
                coeff_sum += g[i] * h[j]
        
        if k <= d:
            expected = f_coeffs[d - k] % m
        else:
            expected = 0
            
        solver.add(coeff_sum % m == expected)
        
    def is_unit_cond(poly):
        primes = []
        temp = m
        for i in range(2, int(math.isqrt(temp)) + 2):
            if temp % i == 0:
                primes.append(i)
                while temp % i == 0: temp //= i
        if temp > 1: primes.append(temp)
        
        allowed_c0 = [i for i in range(m) if math.gcd(i, m) == 1]
        if not allowed_c0:
            c0_cond = z3.BoolVal(False)
        else:
            c0_cond = z3.Or([poly[0] == val for val in allowed_c0])
            
        rad = 1
        for p in primes:
            rad *= p
            
        nilp_conds = [poly[i] % rad == 0 for i in range(1, len(poly))]
        
        if not nilp_conds:
            return c0_cond
        return z3.And(c0_cond, *nilp_conds)
        
    solver.add(z3.Not(is_unit_cond(g)))
    solver.add(z3.Not(is_unit_cond(h)))
    
    solver.add(z3.Or([g[i] != 0 for i in range(max_deg + 1)]))
    solver.add(z3.Or([h[i] != 0 for i in range(max_deg + 1)]))
    
    result = solver.check()
    return result == z3.unsat

def check_in_ideal(poly_coeffs, f_coeffs, m):
    poly_coeffs = list(poly_coeffs)
    f_coeffs = list(f_coeffs)
    
    while poly_coeffs and poly_coeffs[0] % m == 0:
        poly_coeffs.pop(0)
    if not poly_coeffs:
        return True
        
    while f_coeffs and f_coeffs[0] % m == 0:
        f_coeffs.pop(0)
    if not f_coeffs:
        return False
        
    deg_p = len(poly_coeffs) - 1
    deg_f = len(f_coeffs) - 1
    
    max_deg_q = max(0, deg_p) + 2
    
    solver = z3.Solver()
    sid = id(solver)
    Q = [z3.Int(f'Q_{sid}_{i}') for i in range(max_deg_q + 1)]
    for i in range(max_deg_q + 1):
        solver.add(Q[i] >= 0, Q[i] < m)
        
    for k in range(deg_f + max_deg_q + 1):
        coeff_sum = 0
        for i in range(deg_f + 1):
            j = k - i
            if 0 <= j <= max_deg_q:
                f_i = f_coeffs[deg_f - i] % m
                coeff_sum += f_i * Q[j]
                
        if k <= deg_p:
            expected = poly_coeffs[deg_p - k] % m
        else:
            expected = 0
            
        solver.add(coeff_sum % m == expected)
        
    return solver.check() == z3.sat

def poly_mul(A, B, m):
    if not A or not B: return []
    deg_A = len(A) - 1
    deg_B = len(B) - 1
    res = [0] * (deg_A + deg_B + 1)
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            res[i+j] = (res[i+j] + a * b) % m
    while res and res[0] % m == 0:
        res.pop(0)
    return res

def poly_eq(A, B, m):
    A_clean = []
    for a in A:
        if A_clean or a % m != 0:
            A_clean.append(a % m)
    B_clean = []
    for b in B:
        if B_clean or b % m != 0:
            B_clean.append(b % m)
    return A_clean == B_clean

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        if not isinstance(witness, dict):
            return [False, False]
            
        m = witness.get('m', 0)
        f = witness.get('f', [])
        
        if m < 2 or not f or len(f) > 10 or m > 100:
            return [False, False]
            
        f_clean = []
        for c in f:
            if f_clean or c % m != 0:
                f_clean.append(c % m)
        if not f_clean:
            return [False, False]
            
        try:
            h1_ok = is_primitive(f_clean, m)
        except Exception:
            h1_ok = False
            
        try:
            if math.gcd(f_clean[0], m) == 1:
                is_irred = check_irreducible(f_clean, m)
                
                A = witness.get('A', [])
                B = witness.get('B', [])
                Q = witness.get('Q', [])
                
                if A and B:
                    AB = poly_mul(A, B, m)
                    fQ = poly_mul(f_clean, Q, m)
                    
                    if poly_eq(AB, fQ, m):
                        A_in_f = check_in_ideal(A, f_clean, m)
                        B_in_f = check_in_ideal(B, f_clean, m)
                        
                        is_not_prime = (not A_in_f) and (not B_in_f)
                        if is_not_prime:
                            is_prime = False
                            neg_q_ok = not (is_prime == is_irred)
        except Exception:
            neg_q_ok = False
            
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ['H_1: f is primitive', 'neg_Q: conclusion fails']
N_HYP = 1
NEG_Q_INDEX = 1