import sympy
from sympy import Poly
from sympy.abc import x
from sympy.ntheory import isprime, factorint
import itertools

# Top-level setup
# The witness is expected to be a tuple (q, f_coeffs, alpha_coeffs) or a dict with these keys,
# where q is a prime (size of the finite field F_q),
# f_coeffs is a list of integers representing the coefficients of a polynomial f(x) 
# such that E = F_q[x]/(f(x)), and alpha_coeffs represents the element alpha in E.

def is_prime_power(q):
    if not isinstance(q, int) or q < 2:
        return False
    return len(factorint(q)) == 1

def is_valid_algebra(f_coeffs, alpha_coeffs):
    if not isinstance(f_coeffs, list) or not isinstance(alpha_coeffs, list):
        return False
    if len(f_coeffs) < 2 or f_coeffs[0] == 0:
        return False
    if not all(isinstance(c, int) for c in f_coeffs):
        return False
    if not all(isinstance(c, int) for c in alpha_coeffs):
        return False
    return True

def pow_poly(base, exp, mod, domain):
    res = Poly(1, x, domain=domain)
    base = base.rem(mod)
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base).rem(mod)
        base = (base * base).rem(mod)
        exp //= 2
    return res

def compute_trace(alpha, f, q, Fq):
    n = f.degree()
    trace = 0
    for i in range(n):
        xi = Poly(x**i, x, domain=Fq)
        prod = (xi * alpha).rem(f)
        
        coeffs = prod.all_coeffs()
        if i < len(coeffs):
            c = int(coeffs[-(i + 1)])
        else:
            c = 0
            
        trace = (trace + c) % q
    return trace

def has_beta(alpha, f, q, Fq):
    n = f.degree()
    
    if q**n > 10000:
        raise ValueError("State space too large")
        
    alpha_rem = alpha.rem(f)
    
    for coeffs in itertools.product(range(q), repeat=n):
        beta = Poly(coeffs, x, domain=Fq)
        beta_q = pow_poly(beta, q, f, Fq)
        diff = (beta_q - beta).rem(f)
        
        if diff == alpha_rem:
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            f_coeffs = witness.get('f_coeffs')
            alpha_coeffs = witness.get('alpha_coeffs')
        elif isinstance(witness, tuple) and len(witness) == 3:
            q, f_coeffs, alpha_coeffs = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    try:
        h2 = is_valid_algebra(f_coeffs, alpha_coeffs)
    except Exception:
        h2 = False
        
    neg_q = False
    # We restrict the evaluation of the conclusion to prime q for simplicity of polynomial arithmetic.
    # If q is a prime power but not prime, neg_q remains False, prompting the search for a prime q.
    if h1 and h2 and isprime(q):
        try:
            Fq = sympy.GF(q)
            f = Poly(f_coeffs, x, domain=Fq)
            alpha = Poly(alpha_coeffs, x, domain=Fq)
            
            if not f.is_zero and f.degree() >= 1:
                trace = compute_trace(alpha, f, q, Fq)
                beta_exists = has_beta(alpha, f, q, Fq)
                neg_q = (trace == 0) != beta_exists
        except Exception:
            pass
            
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: alpha is in E",
    "¬Q: Tr(alpha) == 0 is not equivalent to exists beta such that alpha = beta^q - beta"
]

N_HYP = 2
NEG_Q_INDEX = 2