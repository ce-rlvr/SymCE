import sympy
from sympy import diff, Poly
from sympy.abc import x

def conditions(witness):
    try:
        p, k, f, r = witness
    except Exception:
        return [False] * 5
        
    # H1: k is a positive integer
    try:
        h1 = isinstance(k, (int, sympy.Integer)) and int(k) > 0
    except Exception:
        h1 = False
        
    # H2: f(x) is a polynomial with integer coefficients
    try:
        poly_f = Poly(f, x)
        h2 = poly_f.domain.is_ZZ
    except Exception:
        h2 = False
        
    # H3: r is an integer such that f(r) ≡ 0 (mod p^k)
    try:
        if not (isinstance(r, (int, sympy.Integer)) and isinstance(p, (int, sympy.Integer))):
            h3 = False
        else:
            p_int = int(p)
            k_int = int(k)
            r_int = int(r)
            val = int(poly_f.eval(r_int))
            mod = abs(p_int**k_int)
            h3 = (mod != 0) and (val % mod == 0)
    except Exception:
        h3 = False
        
    # H4: The formal derivative f'(r) is not divisible by p
    try:
        p_int = int(p)
        r_int = int(r)
        f_prime = diff(f, x)
        poly_f_prime = Poly(f_prime, x)
        val_prime = int(poly_f_prime.eval(r_int))
        h4 = (p_int != 0) and (val_prime % abs(p_int) != 0)
    except Exception:
        h4 = False
        
    # ¬Q: There does not exist a unique integer s modulo p^{k+1} such that f(s) ≡ 0 (mod p^{k+1}) and s ≡ r (mod p^k)
    try:
        p_int = int(p)
        k_int = int(k)
        r_int = int(r)
        valid_s_count = 0
        modulus = abs(p_int**(k_int+1))
        if modulus == 0:
            neg_q = False
        else:
            # Check all possible values of s modulo p^{k+1} that satisfy s ≡ r (mod p^k)
            for m in range(abs(p_int)):
                s = (r_int + m * (p_int**k_int)) % modulus
                if int(poly_f.eval(s)) % modulus == 0:
                    valid_s_count += 1
            neg_q = (valid_s_count != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "H_2: f(x) is a polynomial with integer coefficients",
    "H_3: r is an integer such that f(r) ≡ 0 (mod p^k)",
    "H_4: f'(r) is not divisible by p",
    "¬Q: There does not exist a unique integer s modulo p^{k+1} such that f(s) ≡ 0 (mod p^{k+1}) and s ≡ r (mod p^k)"
]

N_HYP = 4
NEG_Q_INDEX = 4