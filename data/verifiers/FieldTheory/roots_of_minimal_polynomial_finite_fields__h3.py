import sympy
from sympy import Poly, GF
from sympy.abc import x
from sympy.ntheory import isprime, factorint

def poly_powmod(base, exp, mod_poly):
    domain = base.domain
    res = Poly(1, base.gen, domain=domain)
    base = base % mod_poly
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod_poly
        base = (base * base) % mod_poly
        exp //= 2
    return res

def make_poly(coeffs, var, domain):
    if not coeffs:
        return Poly(0, var, domain=domain)
    return Poly(list(reversed(coeffs)), var, domain=domain)

def conditions(witness):
    # H_1: F_q is a finite field with q elements
    try:
        p = witness.get('p', 0)
        q = witness.get('q', 0)
        h1_ok = False
        if isprime(p) and q >= p:
            factors = factorint(q)
            if len(factors) == 1 and p in factors:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: alpha is an element of an extension field F_{q^n}
    try:
        p = witness.get('p', 0)
        q = witness.get('q', 0)
        n = witness.get('n', 0)
        domain = GF(p)
        mod_coeffs = witness.get('mod_poly', [])
        mod_poly = make_poly(mod_coeffs, x, domain)
        
        h2_ok = False
        if n >= 1 and isprime(p) and q >= p:
            factors = factorint(q)
            if len(factors) == 1 and p in factors:
                k = factors[p]
                if mod_poly.degree() == k * n and mod_poly.is_irreducible:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # H_3: d is the degree of m(x)
    try:
        p = witness.get('p', 0)
        q = witness.get('q', 0)
        domain = GF(p)
        mod_coeffs = witness.get('mod_poly', [])
        mod_poly = make_poly(mod_coeffs, x, domain)
        
        m_coeffs = witness.get('m_poly', [])
        h3_ok = False
        if m_coeffs:
            m_norm = []
            for c in m_coeffs:
                if isinstance(c, int):
                    m_norm.append([c])
                elif isinstance(c, list):
                    m_norm.append(c)
                else:
                    raise ValueError
                    
            # Strip leading zeros (trailing in our lowest-degree-first representation)
            while m_norm and make_poly(m_norm[-1], x, domain) % mod_poly == 0:
                m_norm.pop()
                
            if m_norm:
                all_in_Fq = True
                for c_coeffs in m_norm:
                    c_poly = make_poly(c_coeffs, x, domain)
                    # Check if coefficient is in F_q by checking c^q == c
                    c_q = poly_powmod(c_poly, q, mod_poly)
                    if (c_q - c_poly) % mod_poly != 0:
                        all_in_Fq = False
                        break
                h3_ok = all_in_Fq
    except Exception:
        h3_ok = False

    # neg_Q: The conclusion fails
    try:
        p = witness.get('p', 0)
        q = witness.get('q', 0)
        domain = GF(p)
        mod_coeffs = witness.get('mod_poly', [])
        mod_poly = make_poly(mod_coeffs, x, domain)
        
        alpha_coeffs = witness.get('alpha_poly', [])
        alpha_poly = make_poly(alpha_coeffs, x, domain) % mod_poly
        
        m_coeffs = witness.get('m_poly', [])
        m_norm = []
        for c in m_coeffs:
            if isinstance(c, int):
                m_norm.append([c])
            elif isinstance(c, list):
                m_norm.append(c)
                
        while m_norm and make_poly(m_norm[-1], x, domain) % mod_poly == 0:
            m_norm.pop()
            
        d = len(m_norm) - 1
        if d < 0:
            neg_q_ok = False
        else:
            S = []
            current = alpha_poly
            for _ in range(d):
                S.append(current)
                current = poly_powmod(current, q, mod_poly)
                
            S_canon = [tuple(poly.all_coeffs()) for poly in S]
            if len(set(S_canon)) != d:
                neg_q_ok = True
            else:
                all_roots = True
                for root_poly in S:
                    val = Poly(0, x, domain=domain)
                    root_pow = Poly(1, x, domain=domain)
                    for c_coeffs in m_norm:
                        c_poly = make_poly(c_coeffs, x, domain)
                        term = (c_poly * root_pow) % mod_poly
                        val = (val + term) % mod_poly
                        root_pow = (root_pow * root_poly) % mod_poly
                    if val != 0:
                        all_roots = False
                        break
                neg_q_ok = not all_roots
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: alpha is an element of an extension field F_{q^n}",
    "H_3: d is the degree of m(x)",
    "¬Q: m(x) does not split completely or its roots are not exactly the d distinct elements alpha, alpha^q, ..., alpha^{q^{d-1}}"
]

N_HYP = 3
NEG_Q_INDEX = 3