import sympy

# Top-level setup
# (No specific named bindings required for this field theory conjecture, 
# but we define a symbol for polynomial evaluation if needed)
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a tuple (K, a) where K is either a prime p 
        # (representing GF(p)) or a sympy finite field domain, and a is an element of K.
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        
        K_obj, a_obj = witness
        
        # Extract the characteristic p
        if hasattr(K_obj, 'characteristic'):
            p = K_obj.characteristic()
        elif hasattr(K_obj, 'char'):
            p = K_obj.char
        else:
            p = int(K_obj)
            
    except Exception:
        return [False, False, False]

    # H_1: K is a field of characteristic p > 0
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: a is an element of K
    try:
        if isinstance(K_obj, int) or (hasattr(K_obj, 'is_integer') and K_obj.is_integer):
            h2 = isinstance(a_obj, int) or (hasattr(a_obj, 'is_integer') and a_obj.is_integer)
        else:
            h2 = (a_obj in K_obj) or isinstance(a_obj, int) or (hasattr(a_obj, 'is_integer') and a_obj.is_integer)
        h2 = bool(h2)
    except Exception:
        h2 = False

    # ¬Q: The splitting field of x^p - x - a over K does NOT have degree p over K.
    # By Artin-Schreier theory, x^p - x - a either splits completely in K (degree 1) 
    # or is irreducible over K (degree p). 
    # Thus, the degree is NOT p if and only if the polynomial has a root in K.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            has_root = False
            if isinstance(K_obj, int) or (hasattr(K_obj, 'is_integer') and K_obj.is_integer):
                # K is implicitly GF(p)
                a_val = int(a_obj)
                has_root = (a_val % p == 0)
            else:
                # K is a sympy domain
                f = sympy.Poly(x**p - x - a_obj, x, domain=K_obj)
                roots = f.ground_roots()
                has_root = len(roots) > 0
            neg_q = bool(has_root)
    except Exception:
        # Fallback for simple integer representations
        try:
            a_val = int(a_obj)
            neg_q = bool(a_val % p == 0)
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic p > 0",
    "H_2: a is an element of K",
    "¬Q: The splitting field of x^p - x - a over K does not have degree p over K"
]

N_HYP = 2
NEG_Q_INDEX = 2