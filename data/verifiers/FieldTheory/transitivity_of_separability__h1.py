import sympy
from sympy import Poly, sympify
from sympy.abc import x
from sympy.ntheory import isprime

def conditions(witness):
    """
    Witness should be a dictionary with keys 'p', 'f', 'g', 'h' representing
    the characteristic p, and the algebra maps K->L, L->M, K->M respectively.
    K = F_p(t), L = F_p(u), M = F_p(v).
    f is a polynomial representing the image of t in L.
    g is a polynomial representing the image of u in M.
    h is a polynomial representing the image of t in M.
    
    The missing hypothesis in the conjecture is that the extensions form a 
    scalar tower (i.e., the K-algebra structure on M is induced by L).
    Without it, one can define incompatible algebra maps.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            f = witness.get('f')
            g = witness.get('g')
            h = witness.get('h')
        else:
            p, f, g, h = witness
            
        p = int(p)
        if not isprime(p):
            return [False, False, False]
            
        f = sympify(f)
        g = sympify(g)
        h = sympify(h)
        
        syms = f.free_symbols | g.free_symbols | h.free_symbols
        sym = list(syms)[0] if syms else x
        
        f_poly = Poly(f, sym, domain='ZZ')
        g_poly = Poly(g, sym, domain='ZZ')
        h_poly = Poly(h, sym, domain='ZZ')
        
        def is_valid_ext(poly):
            coeffs = poly.all_coeffs()
            if len(coeffs) < 2:
                return False
            # Check if the polynomial has degree >= 1 over F_p
            return any(c % p != 0 for c in coeffs[:-1])
            
        if not is_valid_ext(f_poly) or not is_valid_ext(g_poly) or not is_valid_ext(h_poly):
            return [False, False, False]
            
        # H1: L is a separable extension of K
        # True if the derivative of f is not identically zero mod p
        df = f_poly.diff()
        h1 = any(c % p != 0 for c in df.all_coeffs())
        
        # H2: M is a separable extension of L
        # True if the derivative of g is not identically zero mod p
        dg = g_poly.diff()
        h2 = any(c % p != 0 for c in dg.all_coeffs())
        
        # neg_Q: M is NOT a separable extension of K
        # True if the derivative of h is identically zero mod p (purely inseparable)
        dh = h_poly.diff()
        neg_q = all(c % p == 0 for c in dh.all_coeffs())
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L is a separable extension of K",
    "H_2: M is a separable extension of L",
    "¬Q: M is not a separable extension of K"
]

N_HYP = 2
NEG_Q_INDEX = 2