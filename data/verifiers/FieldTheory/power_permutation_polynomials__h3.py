import sympy
import math
import itertools

x = sympy.Symbol('x')
a = sympy.Symbol('a')

def is_bijection(f, q):
    q_val = int(q)
    if q_val > 1000:
        raise ValueError("q is too large for fast verification")
        
    factors = sympy.ntheory.factorint(q_val)
    p = list(factors.keys())[0]
    k = factors[p]
    
    if k == 1:
        vals = set()
        for i in range(p):
            val = f.subs(x, i)
            val = int(val) % p
            vals.add(val)
        return len(vals) == p
    else:
        irred_expr = None
        for coeffs in itertools.product(range(p), repeat=k):
            poly_expr = a**k + sum(c * a**i for i, c in enumerate(coeffs))
            poly = sympy.Poly(poly_expr, a, domain=sympy.GF(p))
            if poly.is_irreducible:
                irred_expr = poly_expr
                break
        
        if irred_expr is None:
            raise ValueError("Could not find irreducible polynomial")
            
        irred_poly = sympy.Poly(irred_expr, a, domain=sympy.GF(p))
        
        elements = []
        for coeffs in itertools.product(range(p), repeat=k):
            elem = sum(c * a**i for i, c in enumerate(coeffs))
            elements.append(elem)
            
        vals = set()
        for elem in elements:
            val_expr = sympy.expand(f.subs(x, elem))
            val_poly = sympy.Poly(val_expr, a, domain=sympy.GF(p))
            rem = val_poly % irred_poly
            rem_expr = rem.as_expr()
            vals.add(rem_expr)
        return len(vals) == p**k

def conditions(witness):
    try:
        q, n, f = witness
    except Exception:
        return [False, False, False]
        
    # H1: q is a prime power (size of a finite field)
    try:
        q_val = int(q)
        if q_val < 2 or q_val != q:
            h1 = False
        else:
            factors = sympy.ntheory.factorint(q_val)
            h1 = len(factors) == 1
    except Exception:
        h1 = False
        
    # H2: n is a positive integer
    try:
        n_val = int(n)
        h2 = (n_val > 0 and n_val == n)
    except Exception:
        h2 = False
        
    # neg_Q: f(x) induces a bijection on F_q iff gcd(n, q-1) == 1
    try:
        f = sympy.sympify(f)
        
        # Check if f is a polynomial
        try:
            sympy.Poly(f, x, a)
            is_poly = True
        except Exception:
            try:
                sympy.Poly(f, x)
                is_poly = True
            except Exception:
                is_poly = False
                
        if not is_poly:
            neg_q = False
        else:
            bijection = is_bijection(f, q)
            gcd_cond = math.gcd(int(n), int(q) - 1) == 1
            neg_q = (bijection != gcd_cond)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: q is a prime power (size of a finite field)",
    "H_2: n is a positive integer",
    "¬Q: f(x) induces a bijection on F_q does NOT hold if and only if gcd(n, q-1) == 1"
]

N_HYP = 2
NEG_Q_INDEX = 2