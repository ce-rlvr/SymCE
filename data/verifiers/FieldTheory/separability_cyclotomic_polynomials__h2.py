import sympy
from sympy import Symbol, Poly, cyclotomic_poly, diff
from sympy.polys.domains import GF, QQ
from sympy.ntheory import isprime

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "For any positive integer n, the n-th cyclotomic polynomial is separable over any field K."
    
    The witness should be a tuple (n, p), where:
      - n is the index of the cyclotomic polynomial.
      - p is the characteristic of the field K (0 for Q, or a prime for GF(p)).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        n, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # H_2: K is a valid field (represented by characteristic p, where p is 0 or prime)
    try:
        h2 = (isinstance(p, int) or isinstance(p, sympy.Integer)) and (p == 0 or isprime(p))
    except Exception:
        h2 = False
        
    # ¬Q: Phi_n(x) is NOT separable over K (meaning it has repeated roots in its splitting field)
    # A polynomial is not separable iff it shares a common root with its formal derivative,
    # which is equivalent to gcd(f, f') having degree > 0 over K.
    try:
        f_expr = cyclotomic_poly(n, x)
        df_expr = diff(f_expr, x)
        
        if p > 0:
            domain = GF(p)
        else:
            domain = QQ
            
        f_poly = Poly(f_expr, x, domain=domain)
        df_poly = Poly(df_expr, x, domain=domain)
        
        g_poly = f_poly.gcd(df_poly)
        neg_q = g_poly.degree() > 0
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: K is a valid field (witness provides characteristic p, where p is 0 or prime)",
    "¬Q: Phi_n(x) is not separable over K (has repeated roots)"
]

N_HYP = 2
NEG_Q_INDEX = 2