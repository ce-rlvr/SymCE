import sympy
from sympy import Poly
from sympy.abc import x

# Top-level setup
# K is implicitly taken as the field of rational numbers QQ.
# The witness is expected to be a tuple: (poly_expr, n, auto_expr)
# where:
#   - poly_expr is a SymPy expression in x defining the extension L = QQ[x]/(poly_expr)
#   - n is the degree of the extension
#   - auto_expr is a SymPy expression in x representing a generator of the Galois group

def conditions(witness):
    if not isinstance(witness, (list, tuple)) or len(witness) != 3:
        return [False, False, False, False]
        
    poly_expr, n, auto_expr = witness
    
    # H_1: K is a field
    # We use K = QQ implicitly, which is a field.
    h1 = True
    
    # H_2: n is a positive integer such that char(K) does not divide n
    # Since char(QQ) = 0, it does not divide any positive integer.
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False
        
    # H_3: L/K is a finite cyclic Galois extension of degree n
    h3 = False
    try:
        poly = Poly(poly_expr, x, domain='QQ')
        if poly.degree() == n and poly.is_irreducible:
            auto = Poly(auto_expr, x, domain='QQ')
            
            # Helper to compute p1(p2(x)) mod mod_poly
            def compose_mod(p1, p2, mod_poly):
                res = Poly(0, x, domain='QQ')
                p2_pow = Poly(1, x, domain='QQ')
                for c in reversed(p1.all_coeffs()):
                    if c != 0:
                        res = (res + p2_pow * c) % mod_poly
                    p2_pow = (p2_pow * p2) % mod_poly
                return res
            
            # Check if auto is a valid endomorphism (maps a root to a root)
            if compose_mod(poly, auto, poly).is_zero:
                curr = Poly(x, x, domain='QQ')
                order_ok = True
                
                # Check that the order of the automorphism is exactly n
                for i in range(1, n):
                    curr = compose_mod(curr, auto, poly)
                    if curr == Poly(x, x, domain='QQ'):
                        order_ok = False
                        break
                
                if order_ok:
                    curr = compose_mod(curr, auto, poly)
                    if curr == Poly(x, x, domain='QQ'):
                        h3 = True
    except Exception:
        h3 = False
        
    # ¬Q: The conclusion fails at the witness.
    # The conclusion states there exists 'a' in K such that L = K(a^(1/n)) and x^n - a is irreducible.
    # For K = QQ, if L = QQ(a^(1/n)) is a cyclic Galois extension of degree n, 
    # then QQ(a^(1/n)) must contain the primitive n-th root of unity.
    # Since QQ only contains primitive 1st and 2nd roots of unity, no such 'a' can exist for n > 2.
    # Thus, the conclusion is mathematically false for any valid cyclic extension over QQ of degree n > 2.
    try:
        neg_q = (n > 2)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n is a positive integer such that char(K) does not divide n",
    "H_3: L/K is a finite cyclic Galois extension of degree n",
    "¬Q: There is no a in K such that L = K(a^(1/n)) and x^n - a is irreducible"
]

N_HYP = 3
NEG_Q_INDEX = 3