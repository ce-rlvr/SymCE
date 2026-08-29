import sympy
import math

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the false conjecture 
    related to Schönemann's Irreducibility Criterion.
    
    Witness is expected to be a tuple: (f, g, m, n, p)
    or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            m = witness.get('m')
            n = witness.get('n')
            p = witness.get('p')
        else:
            f, g, m, n, p = witness
    except Exception:
        return [False] * 6

    # H_1: f(x) = g(x)^n + p m(x) is a polynomial in Z
    try:
        f_expr = sympy.sympify(f)
        g_expr = sympy.sympify(g)
        m_expr = sympy.sympify(m)
        n_val = int(n)
        p_val = int(p)
        
        f_poly = sympy.Poly(f_expr, x, domain='ZZ')
        g_poly = sympy.Poly(g_expr, x, domain='ZZ')
        m_poly = sympy.Poly(m_expr, x, domain='ZZ')
        
        if n_val >= 1 and p_val >= 2:
            expected_f = g_expr**n_val + p_val * m_expr
            h1 = bool(sympy.expand(f_expr - expected_f) == 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: g(x) in Z is monic
    try:
        h2 = bool(g_poly.LC() == 1)
    except Exception:
        h2 = False

    # H_3: g(x) mod p is irreducible
    try:
        coeffs = [c % p_val for c in g_poly.all_coeffs()]
        # Remove leading zeros mod p
        while coeffs and coeffs[0] == 0:
            coeffs.pop(0)
            
        if not coeffs:
            h3 = False
        else:
            if sympy.isprime(p_val):
                g_mod = sympy.Poly(coeffs, x, domain=sympy.GF(p_val))
                if g_mod.degree() <= 0:
                    h3 = False
                else:
                    factors = sympy.factor_list(g_mod)
                    # Irreducible if exactly one factor with multiplicity 1
                    h3 = bool(len(factors[1]) == 1 and factors[1][0][1] == 1)
            else:
                # For composite p, we only accept monic degree 1 polynomials 
                # as they are mathematically guaranteed to be irreducible.
                deg = len(coeffs) - 1
                if deg == 1 and coeffs[0] == 1:
                    h3 = True
                else:
                    h3 = False
    except Exception:
        h3 = False

    # H_4: deg(m) < n deg(g)
    try:
        if m_poly.is_zero:
            deg_m = -1
        else:
            deg_m = m_poly.degree()
        deg_g = g_poly.degree()
        h4 = bool(deg_m < n_val * deg_g)
    except Exception:
        h4 = False

    # H_5: m(x) mod p is not divisible by g(x) mod p
    try:
        # Since g(x) is monic, polynomial division over ZZ is exact and matches division over Z/pZ
        _, r_poly = m_poly.div(g_poly)
        h5 = False
        for c in r_poly.all_coeffs():
            if c % p_val != 0:
                h5 = True
                break
    except Exception:
        h5 = False

    # not Q: f(x) is reducible in Q
    try:
        factors = sympy.factor_list(f_expr, domain='QQ')
        # It is irreducible if there is exactly one non-constant factor with multiplicity 1
        is_irreducible = (len(factors[1]) == 1 and factors[1][0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: f is g^n + p m in Z",
    "H_2: g is monic",
    "H_3: g mod p is irreducible",
    "H_4: deg m < n deg g",
    "H_5: m mod p not divisible by g mod p",
    "not Q: f is reducible in Q"
]

N_HYP = 5
NEG_Q_INDEX = 5