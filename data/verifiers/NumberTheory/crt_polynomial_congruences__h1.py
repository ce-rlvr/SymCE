import sympy
from sympy.abc import x
from sympy.polys.polytools import Poly

# Top-level setup
# The witness should be a tuple (f, m, n) where f is a polynomial expression in x,
# and m, n are integers.

def conditions(witness) -> list[bool]:
    try:
        f, m, n = witness
        f = sympy.sympify(f)
        m = sympy.sympify(m)
        n = sympy.sympify(n)
    except Exception:
        return [False, False]
        
    # H1: f(x) is a polynomial with integer coefficients
    try:
        if not (m.is_Integer and n.is_Integer):
            h1 = False
        else:
            poly_f = Poly(f, x)
            h1 = all(c.is_Integer for c in poly_f.coeffs())
    except Exception:
        h1 = False
        
    # neg_Q: The equivalence fails
    # The equivalence is: f(x) == 0 mod mn for all x <==> f(x) == 0 mod m and mod n for all x.
    # Since A (mod mn) always implies B (mod m and mod n), the equivalence fails
    # if and only if B is True and A is False.
    try:
        if not (m.is_Integer and n.is_Integer) or m == 0 or n == 0:
            neg_q = False
        else:
            m_int = abs(int(m))
            n_int = abs(int(n))
            mn_int = m_int * n_int
            
            if mn_int > 1000000:
                neg_q = False  # Prevent excessive evaluation time
            else:
                # Fast polynomial evaluation using Horner's method
                coeffs = [int(c) for c in Poly(f, x).all_coeffs()]
                def eval_poly(val):
                    res = 0
                    for c in coeffs:
                        res = res * val + c
                    return res
                
                B_m = all(eval_poly(i) % m_int == 0 for i in range(m_int))
                B_n = all(eval_poly(i) % n_int == 0 for i in range(n_int))
                B = B_m and B_n
                
                if B:
                    A = all(eval_poly(i) % mn_int == 0 for i in range(mn_int))
                    neg_q = not A
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial with integer coefficients",
    "¬Q: f(x) ≡ 0 mod m and mod n for all x, but NOT ≡ 0 mod mn for all x"
]

N_HYP = 1
NEG_Q_INDEX = 1