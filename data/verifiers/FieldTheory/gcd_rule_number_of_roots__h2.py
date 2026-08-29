import sympy
from sympy import Symbol, Poly

# Top-level setup
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "¬Q: The number of distinct roots of f(x) in F_q is NOT equal to the degree of gcd(f(x), x^q - x)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (q, f) where q is an integer and f is a SymPy expression in x,
    checks if it is a valid counterexample to the false conjecture.
    """
    try:
        q, f = witness
    except Exception:
        return [False, False]
    
    # H_1: F_q is a finite field with q elements
    # This requires q to be a prime power (q >= 2).
    try:
        if not isinstance(q, int) or q < 2:
            h1 = False
        else:
            factors = sympy.ntheory.factorint(q)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # ¬Q: The number of distinct roots of f(x) in F_q is NOT equal to the degree of gcd(f(x), x^q - x)
    try:
        # Try to create polynomials over GF(q)
        try:
            domain = sympy.GF(q)
            f_poly = Poly(f, x, domain=domain)
            xq_minus_x = Poly(x**q - x, x, domain=domain)
        except Exception:
            # Fallback to GF(p) if q is a prime power p^k and GF(q) initialization fails
            factors = sympy.ntheory.factorint(q)
            p = list(factors.keys())[0]
            domain = sympy.GF(p)
            f_poly = Poly(f, x, domain=domain)
            xq_minus_x = Poly(x**q - x, x, domain=domain)
            
        if f_poly.is_zero:
            # In formal systems (like Lean/Isabelle), the set of roots of the zero polynomial 
            # is defined as empty to keep it finite. So the number of distinct roots is 0.
            # However, gcd(0, x^q - x) = x^q - x, which has degree q.
            # Since q >= 2, 0 != q. Thus the conclusion fails.
            neg_q = True
        else:
            g = f_poly.gcd(xq_minus_x)
            deg_gcd = g.degree()
            
            # Count distinct roots in F_q
            factors = sympy.ntheory.factorint(q)
            if len(factors) == 1 and list(factors.keys())[0] == q:
                # If q is prime, we can simply evaluate at all elements of F_q
                roots = set()
                for i in range(q):
                    if f_poly.eval(i) == 0:
                        roots.add(i)
                num_roots = len(roots)
            else:
                # For prime powers, mathematically num_roots == deg_gcd for any non-zero f
                num_roots = deg_gcd
                
            neg_q = bool(num_roots != deg_gcd)
    except Exception:
        neg_q = False

    return [h1, neg_q]