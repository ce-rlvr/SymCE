import sympy
from sympy import QQ, GF, ZZ

def is_p_th_power(a_K, p, K):
    try:
        x = sympy.Symbol('x')
        poly = x**p - a_K
        factors = sympy.factor_list(poly, domain=K)[1]
        for f, mult in factors:
            if f.degree() == 1:
                return True
        return False
    except Exception:
        return False

def is_in_minus_4_K4(a_K, K):
    try:
        x = sympy.Symbol('x')
        poly = 4 * x**4 + a_K
        factors = sympy.factor_list(poly, domain=K)[1]
        for f, mult in factors:
            if f.degree() == 1:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        K, a, n = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: K is a field
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    # H2: a in K and a not in K^p for all prime factors p of n
    try:
        try:
            a_K = K(a)
            a_in_K = True
        except Exception:
            a_in_K = False
            a_K = a
            
        if not a_in_K:
            h2 = False
        else:
            factors = sympy.factorint(n)
            prime_factors = [p for p in factors.keys() if p > 1]
            h2 = True
            for p in prime_factors:
                if is_p_th_power(a_K, p, K):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # H3: If 4 divides n, then a not in -4K^4
    try:
        h3 = True
        if n % 4 == 0:
            if is_in_minus_4_K4(a_K, K):
                h3 = False
    except Exception:
        h3 = False
        
    # Negated Conclusion: x^n - a is NOT irreducible over K
    try:
        if n <= 0:
            neg_q = True
        else:
            x = sympy.Symbol('x')
            poly = x**n - a_K
            factored = sympy.factor_list(poly, domain=K)
            factors = factored[1]
            if len(factors) == 1 and factors[0][1] == 1 and factors[0][0].degree() == n:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: a in K and a not in K^p for all prime factors p of n",
    "H_3: If 4 divides n, then a not in -4K^4",
    "¬Q: The binomial polynomial x^n - a is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3