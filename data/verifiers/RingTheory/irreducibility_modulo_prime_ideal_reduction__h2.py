import sympy
import math
from itertools import product

x = sympy.Symbol('x')

def check_irreducible_mod(f_poly, m):
    if m < 2:
        return False
        
    f_coeffs = [c % m for c in f_poly.all_coeffs()]
    while f_coeffs and f_coeffs[0] == 0:
        f_coeffs.pop(0)
    if not f_coeffs or f_coeffs == [0]:
        return False

    def is_unit(coeffs):
        if not coeffs or coeffs == [0]: return False
        if math.gcd(coeffs[-1], m) != 1: return False
        primes = sympy.primefactors(m)
        for c in coeffs[:-1]:
            for p in primes:
                if c % p != 0:
                    return False
        return True

    if is_unit(f_coeffs):
        return False

    D = len(f_coeffs)
    if D < 3:
        D = 3
        
    if m ** (D + 1) > 100000:
        return False

    polys = []
    for deg in range(D + 1):
        for coeffs in product(range(m), repeat=deg+1):
            if deg == 0 or coeffs[0] != 0:
                polys.append(list(coeffs))
                
    non_units = [p for p in polys if not is_unit(p)]
    
    non_units_by_last = {i: [] for i in range(m)}
    for p in non_units:
        non_units_by_last[p[-1]].append(p)
        
    f_last = f_coeffs[-1]
    for A in non_units:
        A_last = A[-1]
        for B_last in range(m):
            if (A_last * B_last) % m == f_last:
                for B in non_units_by_last[B_last]:
                    degA = len(A) - 1
                    degB = len(B) - 1
                    res = [0] * (degA + degB + 1)
                    for i in range(degA + 1):
                        for j in range(degB + 1):
                            res[i+j] += A[i] * B[j]
                    
                    res = [c % m for c in res]
                    while res and res[0] == 0:
                        res.pop(0)
                    if not res:
                        res = [0]
                        
                    if res == f_coeffs:
                        return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int):
                m, f_expr = witness
            elif isinstance(witness[1], int):
                f_expr, m = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
            
        if not isinstance(m, int) or m < 2:
            return [False] * 5
            
        f_poly = sympy.Poly(f_expr, x, domain='ZZ')
        coeffs = f_poly.all_coeffs()
        if not coeffs:
            return [False] * 5
            
    except Exception:
        return [False] * 5

    try:
        h1 = True
    except Exception:
        h1 = False

    try:
        g = coeffs[0]
        for c in coeffs[1:]:
            g = math.gcd(g, c)
        h2 = (abs(g) == 1)
    except Exception:
        h2 = False

    try:
        a_n = coeffs[0]
        h3 = (a_n % m != 0)
    except Exception:
        h3 = False

    try:
        h4 = check_irreducible_mod(f_poly, m)
    except Exception:
        h4 = False

    try:
        content, factors = sympy.factor_list(f_poly)
        is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: f is a primitive polynomial",
    "H_3: a_n is not in P",
    "H_4: The reduction of f modulo P is irreducible",
    "~Q: f is reducible over R"
]

N_HYP = 4
NEG_Q_INDEX = 4