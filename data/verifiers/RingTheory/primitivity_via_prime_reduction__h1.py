import sympy
import z3
import math

x = sympy.abc.x
sqrt = sympy.sqrt

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial",
    "not Q: Equivalence fails"
]

def is_divisible(c, p, D):
    a, b = c
    px, py = p
    M = px**2 - D*py**2
    if M == 0: 
        return False
    real_part = a*px - b*py*D
    imag_part = b*px - a*py
    return real_part % M == 0 and imag_part % M == 0

def is_prime_element(p, D):
    px, py = p
    M = px**2 - D*py**2
    if M <= 1:
        return False
        
    f = sympy.factorint(M)
    if len(f) != 1:
        return False
    q, exp = list(f.items())[0]
    if exp > 2:
        return False
        
    if exp == 1:
        return True
        
    if exp == 2:
        if not is_divisible((q, 0), p, D):
            return False
        if q == 2:
            return False
        else:
            return sympy.legendre_symbol(D, q) == -1
            
    return False

def is_primitive(D, coeffs):
    solver = z3.Solver()
    vars = []
    for i in range(len(coeffs)):
        vx = z3.Int(f'x_{id(solver)}_{i}')
        vy = z3.Int(f'y_{id(solver)}_{i}')
        vars.append((vx, vy))
    
    eq1 = sum(c[0]*v[0] + D*c[1]*v[1] for c, v in zip(coeffs, vars)) == 1
    eq2 = sum(c[1]*v[0] + c[0]*v[1] for c, v in zip(coeffs, vars)) == 0
    solver.add(eq1)
    solver.add(eq2)
    return solver.check() == z3.sat

def reduction_nonzero_for_all_primes(D, coeffs):
    norms = [c[0]**2 - D*c[1]**2 for c in coeffs]
    G = norms[0]
    for n in norms[1:]:
        G = math.gcd(G, n)
        
    if G == 0:
        return False
        
    if G == 1:
        return True
        
    divs = set()
    for i in range(1, math.isqrt(G) + 1):
        if G % i == 0:
            divs.add(i)
            divs.add(G // i)
            
    for M in sorted(list(divs)):
        if M <= 1:
            continue
            
        f = sympy.factorint(M)
        if len(f) != 1:
            continue
        q, exp = list(f.items())[0]
        if exp > 2:
            continue
            
        abs_D = abs(D)
        max_y = int(math.isqrt(M // abs_D))
        for y in range(-max_y, max_y + 1):
            rem = M - abs_D * (y**2)
            if rem < 0:
                continue
            px = math.isqrt(rem)
            if px*px == rem:
                for p_x in set([px, -px]):
                    p = (p_x, y)
                    divides_all = True
                    for c in coeffs:
                        if not is_divisible(c, p, D):
                            divides_all = False
                            break
                    if divides_all:
                        if is_prime_element(p, D):
                            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[1], list):
                D, coeffs = witness
                if not isinstance(D, int) or D >= 0:
                    return [False, False]
                for c in coeffs:
                    if not isinstance(c, tuple) or len(c) != 2:
                        return [False, False]
            else:
                f, D = witness
                f = sympy.sympify(f)
                D = int(D)
                if D >= 0:
                    return [False, False]
                poly = sympy.Poly(f, x)
                coeffs_expr = poly.all_coeffs()
                coeffs = []
                sqD = sympy.sqrt(D)
                for c in coeffs_expr:
                    c = sympy.expand(c)
                    a = c.subs(sqD, 0)
                    b = sympy.simplify((c - a) / sqD)
                    if not a.is_Integer or not b.is_Integer:
                        return [False, False]
                    coeffs.append((int(a), int(b)))
        else:
            f = sympy.sympify(witness)
            poly = sympy.Poly(f, x)
            coeffs_expr = poly.all_coeffs()
            D = -5
            for c in coeffs_expr:
                for arg in c.atoms(sympy.Pow):
                    if arg.exp == sympy.Rational(1, 2):
                        D = int(arg.base)
                        break
            if D >= 0:
                return [False, False]
            coeffs = []
            sqD = sympy.sqrt(D)
            for c in coeffs_expr:
                c = sympy.expand(c)
                a = c.subs(sqD, 0)
                b = sympy.simplify((c - a) / sqD)
                if not a.is_Integer or not b.is_Integer:
                    return [False, False]
                coeffs.append((int(a), int(b)))
            
        is_nonzero = any(c[0] != 0 or c[1] != 0 for c in coeffs)
        H_1_ok = is_nonzero
        
        prim = is_primitive(D, coeffs)
        red_nonzero = reduction_nonzero_for_all_primes(D, coeffs)
        
        neg_Q_ok = (prim != red_nonzero)
        
        return [H_1_ok, neg_Q_ok]
    except Exception:
        return [False, False]