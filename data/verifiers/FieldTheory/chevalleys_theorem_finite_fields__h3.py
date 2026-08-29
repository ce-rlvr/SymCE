import sympy
from sympy.ntheory import factorint
import itertools

# Top-level setup for variables commonly used in polynomials
x, y, z, w = sympy.symbols('x y z w')
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = sympy.symbols('x1:11')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for Chevalley's Theorem (with dropped degree hypothesis).
    The witness should be a tuple: (q, vars_list, f)
    where:
      - q is the size of the finite field (must be a prime for this verifier's evaluation)
      - vars_list is a list or tuple of sympy symbols (the variables)
      - f is a sympy expression representing the polynomial
    """
    try:
        q, vars_list, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F_q is a finite field
    try:
        factors = factorint(q)
        # A finite field must have size p^k. 
        h1 = (len(factors) == 1)
    except Exception:
        h1 = False
        
    # H_2: f is a polynomial in n variables
    try:
        f_expr = sympy.sympify(f)
        if len(vars_list) < 1:
            h2 = False
        elif not f_expr.free_symbols.issubset(set(vars_list)):
            h2 = False
        else:
            # Enforce that it is a polynomial with integer coefficients (valid over F_q)
            poly = sympy.Poly(f_expr, *vars_list, domain='ZZ')
            h2 = True
    except Exception:
        h2 = False
        
    # H_3: There exists at least one point where f = 0
    # ¬Q: There is NO other distinct point where f = 0 (i.e., exactly one zero)
    try:
        if not h1 or not h2:
            h3 = False
            neg_q = False
        else:
            p, k = list(factorint(q).items())[0]
            # For simplicity and speed, this verifier only evaluates over prime fields (k=1)
            if k == 1:
                # Prevent excessive evaluation time for unreasonably large fields/dimensions
                if p**len(vars_list) > 10000:
                    h3 = False
                    neg_q = False
                else:
                    zeros = 0
                    for pt in itertools.product(range(p), repeat=len(vars_list)):
                        val = poly(*pt)
                        if int(val) % p == 0:
                            zeros += 1
                            
                    h3 = (zeros >= 1)
                    neg_q = (zeros <= 1)
            else:
                # Evaluation over non-prime finite fields is not supported by this simple verifier
                h3 = False
                neg_q = False
    except Exception:
        h3 = False
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: f is a polynomial in n variables",
    "H_3: There exists at least one point (c_1, ..., c_n) in F_q^n such that f(c_1, ..., c_n) = 0",
    "¬Q: There is NO other distinct point in F_q^n such that f = 0 (exactly one zero)"
]

N_HYP = 3
NEG_Q_INDEX = 3