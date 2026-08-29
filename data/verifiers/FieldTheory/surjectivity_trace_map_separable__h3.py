import sympy
from sympy import Poly, GF, QQ, ZZ, Rational
from sympy.abc import x, t, y, z

def get_domain_int(domain, val):
    try:
        return domain.convert(val)
    except Exception:
        try:
            return domain.from_zz(val)
        except Exception:
            return domain.one * val

def safe_neg(domain, val):
    try:
        return domain.neg(val)
    except Exception:
        return -val

def safe_add(domain, a, b):
    try:
        return domain.add(a, b)
    except Exception:
        return a + b

def safe_mul(domain, a, b):
    try:
        return domain.mul(a, b)
    except Exception:
        return a * b

def check_irreducible(P):
    try:
        res = P.is_irreducible
        if res is not None:
            return res
    except Exception:
        pass
    
    try:
        domain = P.domain
        if hasattr(domain, 'is_FractionField') and domain.is_FractionField:
            if len(domain.gens) == 1:
                gen_sym = domain.gens[0]
                gen_el = domain.from_sympy(gen_sym)
                if P.degree() > 1:
                    c_n = P.nth(P.degree())
                    c_0 = P.nth(0)
                    other_zero = all(P.nth(i) == domain.zero for i in range(1, P.degree()))
                    if other_zero and c_n == domain.one:
                        if c_0 == safe_neg(domain, gen_el) or c_0 == gen_el:
                            return True
    except Exception:
        pass

    try:
        domain = P.domain
        if hasattr(domain, 'is_FractionField') and domain.is_FractionField:
            from sympy import Poly, fraction, cancel
            expr = P.as_expr()
            num, den = fraction(cancel(expr))
            gens = domain.gens + P.gens
            K = domain.domain
            poly_multi = Poly(num, *gens, domain=K)
            return poly_multi.is_irreducible
    except Exception:
        pass
    
    return False

def is_trace_surjective(P):
    n = P.degree()
    if n <= 0:
        return False
        
    domain = P.domain
    coeffs = P.all_coeffs()
    c_n = coeffs[0]
    try:
        c_n_inv = domain.invert(c_n)
        coeffs = [safe_mul(domain, c, c_n_inv) for c in coeffs]
    except Exception:
        coeffs = [c / c_n for c in coeffs]
    
    p_sums = []
    val_n = n
    char = getattr(domain, 'char', 0)
    if char > 0:
        val_n = n % char
    p_sums.append(get_domain_int(domain, val_n))
    
    for k in range(1, n):
        s = domain.zero
        for i in range(1, k):
            term = safe_mul(domain, coeffs[i], p_sums[k - i])
            s = safe_add(domain, s, term)
            
        val_k = k
        if char > 0:
            val_k = k % char
        term2 = safe_mul(domain, get_domain_int(domain, val_k), coeffs[k])
        s = safe_add(domain, s, term2)
        p_sums.append(safe_neg(domain, s))
        
    for p_val in p_sums:
        if not (p_val == domain.zero):
            return True
            
    return False

def conditions(witness):
    # H1: F is a field
    h1_ok = False
    try:
        domain = witness.domain
        h1_ok = bool(domain.is_Field)
    except Exception:
        h1_ok = False
        
    # H2: E is a finite field extension of F
    h2_ok = False
    try:
        if witness.degree() > 0:
            h2_ok = bool(check_irreducible(witness))
    except Exception:
        h2_ok = False
        
    # neg_Q: Trace map is NOT surjective
    neg_q_ok = False
    try:
        surjective = is_trace_surjective(witness)
        neg_q_ok = not surjective
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a finite field extension of F",
    "¬Q: The field trace map Tr_{E/F}: E -> F is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2