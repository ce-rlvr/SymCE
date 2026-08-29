import sympy
from sympy.abc import x, y, z, t, a, b, c

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    """
    witness is expected to be a tuple: (K, p, a)
    where K is a SymPy domain (e.g., sympy.GF(p)), p is an integer, 
    and a is an element (which may or may not be in K).
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        K, p, a_val = witness
    except Exception:
        return [False, False, False]
        
    # H1: K is a field of prime characteristic p > 0
    try:
        h1 = K.is_Field and K.characteristic() == p and sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H2: The polynomial x^p - x - a has no roots in K
    try:
        x_sym = sympy.Symbol('x')
        try:
            f = x_sym**p - x_sym - a_val
            poly_f = sympy.Poly(f, x_sym, domain=K)
            
            # If a_val is in K, we check for roots in K
            if hasattr(K, 'order') and K.order == p:
                has_root = False
                for i in range(p):
                    if poly_f.eval(K(i)) == K.zero:
                        has_root = True
                        break
                h2 = not has_root
            else:
                roots = sympy.roots(poly_f)
                h2 = (len(roots) == 0)
        except Exception:
            # If f construction or Poly fails, a_val is not in K.
            # If a_val is not in K, then c^p - c - a_val cannot be zero for any c in K.
            # Thus f has no roots in K.
            h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The polynomial x^p - x - a is NOT irreducible over K
    try:
        x_sym = sympy.Symbol('x')
        try:
            f = x_sym**p - x_sym - a_val
            poly_f = sympy.Poly(f, x_sym, domain=K)
            neg_q = not poly_f.is_irreducible
        except Exception:
            # If Poly construction fails, a_val is not in K, so f is not in K[x].
            # Therefore, it cannot be irreducible over K.
            neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field of prime characteristic p > 0",
    "H_2: The polynomial x^p - x - a has no roots in K",
    "¬Q: The polynomial x^p - x - a is not irreducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2