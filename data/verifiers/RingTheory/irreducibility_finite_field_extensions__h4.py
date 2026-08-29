import sympy
import math

# Top-level setup
x = sympy.Symbol('x')

def is_prime_power(n):
    try:
        n_val = int(n)
        if n_val != n or n_val <= 1:
            return False
        return len(sympy.factorint(n_val)) == 1
    except Exception:
        return False

def is_irreducible_over_Fq(f, q, m, x_sym):
    """
    Checks if a polynomial f (with integer coefficients) is irreducible over F_{q^m}.
    q must be a prime power p^k.
    """
    try:
        q_val = int(q)
        factors = sympy.factorint(q_val)
        if len(factors) != 1:
            return False
        p, k = list(factors.items())[0]
        
        poly_f_mod = sympy.Poly(f, x_sym, modulus=p)
        deg = poly_f_mod.degree()
        
        if deg < 1:
            return False
            
        # Check irreducibility over F_p
        factored = sympy.factor_list(poly_f_mod)
        if len(factored[1]) != 1 or factored[1][0][1] != 1:
            return False
            
        # For f in F_p[x], it is irreducible over F_{p^{k*m}} iff 
        # it is irreducible over F_p AND gcd(deg(f), k*m) == 1.
        return math.gcd(int(deg), int(k * m)) == 1
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness tuple (q, m, f), checks if it is a valid counterexample.
    """
    try:
        q, m, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F_q is a finite field with q elements (and m >= 1 is an integer)
    try:
        m_val = int(m)
        h1_ok = is_prime_power(q) and m_val == m and m_val >= 1
    except Exception:
        h1_ok = False
        
    # H_2: f(x) is an irreducible polynomial over F_q
    try:
        h2_ok = is_irreducible_over_Fq(f, q, 1, x)
    except Exception:
        h2_ok = False
        
    # H_3: The degree of f(x) is n >= 1
    try:
        poly_f = sympy.Poly(f, x)
        h3_ok = poly_f.degree() >= 1
    except Exception:
        h3_ok = False
        
    # ¬Q: f(x) is not irreducible over the extension field F_{q^m}
    try:
        neg_q_ok = not is_irreducible_over_Fq(f, q, m, x)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: f(x) is an irreducible polynomial over F_q",
    "H_3: The degree of f(x) is n >= 1",
    "¬Q: f(x) is not irreducible over the extension field F_q^m"
]

N_HYP = 3
NEG_Q_INDEX = 3