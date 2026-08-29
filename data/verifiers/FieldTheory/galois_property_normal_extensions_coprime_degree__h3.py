import sympy
from sympy import symbols, expand, rem, Poly, degree, factor_list, collect, cancel, fraction
from sympy.ntheory import isprime

# Top-level setup: define symbols that the witness expression may reference.
# The witness is expected to be a tuple: (p, P, roots)
# where:
#   - p is the characteristic (a prime integer)
#   - P is the minimal polynomial of the extension L = K[X]/(P), given as an expression in X and t
#   - roots is a list of expressions in X and t, representing the roots of P(Y) in L
X, t, Y = symbols('X t Y')

def is_monic(P, X):
    try:
        return Poly(P, X).LC() == 1
    except Exception:
        return False

def reduce_mod(expr, P, X, t, p):
    try:
        expr = expand(expr)
        remainder = rem(expr, P, X)
        if remainder == 0:
            return True
        
        remainder = cancel(remainder)
        num, den = fraction(remainder)
        
        if num == 0:
            return True
            
        poly = Poly(num, X, t)
        for c in poly.coeffs():
            n, d = c.as_numer_denom()
            if n % p != 0:
                return False
        return True
    except Exception:
        return False

def is_irreducible_mod(P, X, t, p):
    try:
        factors = factor_list(P, X, t, modulus=p)
        if len(factors[1]) == 1 and factors[1][0][1] == 1:
            return True
        return False
    except Exception:
        return False

def check_normal(P, roots, X, Y, t, p):
    try:
        prod = 1
        for r in roots:
            prod = prod * (Y - r)
        
        diff = expand(prod - P.subs(X, Y))
        
        collected = collect(diff, Y, evaluate=False)
        for power, coeff in collected.items():
            if not reduce_mod(coeff, P, X, t, p):
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        p, P, roots = witness
    except Exception:
        return [False, False, False]
    
    # H_1: L/K is a finite normal extension
    try:
        h1 = False
        if is_monic(P, X):
            d = degree(P, X)
            if d >= 1:
                if is_irreducible_mod(P, X, t, p):
                    if len(roots) == d:
                        if check_normal(P, roots, X, Y, t, p):
                            h1 = True
    except Exception:
        h1 = False

    # H_2: The characteristic of the field K is p > 0
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # ¬Q: L/K is NOT a Galois extension
    try:
        neg_q = False
        if is_monic(P, X):
            d = degree(P, X)
            distinct_roots = []
            for r in roots:
                is_new = True
                for dr in distinct_roots:
                    if reduce_mod(r - dr, P, X, t, p):
                        is_new = False
                        break
                if is_new:
                    distinct_roots.append(r)
            is_separable = (len(distinct_roots) == d)
            neg_q = not is_separable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite normal extension",
    "H_2: The characteristic of the field K is p > 0",
    "¬Q: L/K is not a Galois extension"
]

N_HYP = 2
NEG_Q_INDEX = 2