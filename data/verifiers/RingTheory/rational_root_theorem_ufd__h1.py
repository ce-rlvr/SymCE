import math
from sympy import sqrt, simplify, Poly, ZZ, expand, gcd, factor_list
from sympy.ntheory import divisors
from sympy.abc import X

# Top-level setup
sqrt_minus_5 = sqrt(-5)

def is_integer(x):
    try:
        return x.is_Integer or (x.is_Rational and x.q == 1)
    except Exception:
        return False

def get_u_v(expr):
    expr = simplify(expr)
    expr_conj = expr.subs(sqrt_minus_5, -sqrt_minus_5)
    u = simplify((expr + expr_conj) / 2)
    v = simplify((expr - expr_conj) / (2 * sqrt_minus_5))
    return u, v

def in_Z_sqrt_minus_5(expr):
    try:
        u, v = get_u_v(expr)
        return is_integer(u) and is_integer(v)
    except Exception:
        return False

def is_coprime_Z_sqrt_minus_5(a, b):
    try:
        u_a, v_a = get_u_v(a)
        u_b, v_b = get_u_v(b)
        norm_a = u_a**2 + 5 * v_a**2
        norm_b = u_b**2 + 5 * v_b**2
        if not (is_integer(norm_a) and is_integer(norm_b)):
            return False
        norm_a = int(norm_a)
        norm_b = int(norm_b)
        g = math.gcd(norm_a, norm_b)
        
        common_divisors = []
        for d in range(1, g + 1):
            if g % d == 0:
                max_v = math.isqrt(d // 5)
                for v in range(-max_v, max_v + 1):
                    rem = d - 5 * v**2
                    if rem >= 0:
                        u = math.isqrt(rem)
                        if u**2 == rem:
                            common_divisors.append(u + v*sqrt_minus_5)
                            if u != 0:
                                common_divisors.append(-u + v*sqrt_minus_5)
        
        for D in common_divisors:
            if in_Z_sqrt_minus_5(simplify(a / D)) and in_Z_sqrt_minus_5(simplify(b / D)):
                u_D, v_D = get_u_v(D)
                if u_D**2 + 5 * v_D**2 != 1:
                    return False
        return True
    except Exception:
        return False

def in_Z_X2_X3(expr):
    try:
        p = Poly(expr, X)
        if p.domain != ZZ:
            return False
        return p.coeff_monomial(X**1) == 0
    except Exception:
        return False

def get_all_divisors_ZX(g):
    try:
        coeff, factors = factor_list(g)
        if not coeff.is_Integer:
            return []
        int_divs = divisors(int(coeff))
        
        poly_divs = [1]
        for f, exp in factors:
            new_divs = []
            for d in poly_divs:
                for i in range(exp + 1):
                    new_divs.append(d * f**i)
            poly_divs = new_divs
            
        all_divs = []
        for i_d in int_divs:
            for p_d in poly_divs:
                all_divs.append(i_d * p_d)
                all_divs.append(-i_d * p_d)
        return all_divs
    except Exception:
        return []

def is_coprime_Z_X2_X3(a, b):
    try:
        g = gcd(a, b)
        divs = get_all_divisors_ZX(g)
        if not divs:
            return False
        for D in divs:
            D = simplify(D)
            if in_Z_X2_X3(D):
                if in_Z_X2_X3(simplify(a / D)) and in_Z_X2_X3(simplify(b / D)):
                    if D != 1 and D != -1:
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        a = witness['a']
        b = witness['b']
        c_list = witness['c_list']
        ring = witness.get('ring', 'Z[sqrt(-5)]')
    except Exception:
        return [False, False, False, False]
        
    if ring == 'Z[sqrt(-5)]':
        in_R = in_Z_sqrt_minus_5
        is_coprime = is_coprime_Z_sqrt_minus_5
    elif ring == 'Z[X^2, X^3]':
        in_R = in_Z_X2_X3
        is_coprime = is_coprime_Z_X2_X3
    else:
        return [False, False, False, False]
        
    # H1: K is the field of fractions of R
    h1 = True
    
    # H2: a and b are elements of R that are coprime
    try:
        h2 = in_R(a) and in_R(b) and is_coprime(a, b)
    except Exception:
        h2 = False
        
    # H3: x = a/b is a root of f(x) and c_i in R
    try:
        if not c_list:
            h3 = False
        else:
            h3 = True
            for c in c_list:
                if not in_R(c):
                    h3 = False
                    break
            if h3:
                b_simp = simplify(b)
                if b_simp == 0:
                    h3 = False
                else:
                    x = simplify(a / b_simp)
                    val = sum(c_list[i] * x**i for i in range(len(c_list)))
                    if simplify(expand(val)) != 0:
                        h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: a does not divide c_0 in R OR b does not divide c_n in R
    try:
        if not c_list:
            neg_q = False
        else:
            c_0 = c_list[0]
            c_n = c_list[-1]
            
            a_simp = simplify(a)
            b_simp = simplify(b)
            
            a_divides_c0 = in_R(simplify(c_0 / a_simp)) if a_simp != 0 else (simplify(c_0) == 0)
            b_divides_cn = in_R(simplify(c_n / b_simp)) if b_simp != 0 else (simplify(c_n) == 0)
            
            neg_q = not (a_divides_c0 and b_divides_cn)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: a and b are elements of R that are coprime",
    "H_3: x = a/b is a root of the polynomial f(x)",
    "\u00acQ: a does not divide c_0 in R, or b does not divide c_n in R"
]

N_HYP = 3
NEG_Q_INDEX = 3