import sympy
import itertools
import math

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that R is an integral domain.
    A valid counterexample can be found in a ring with zero divisors, e.g., Z_m.
    Witness format: (f_expr, p, m) for Z_m, or (f_expr, p) for ZZ.
    """
    try:
        if len(witness) == 3:
            f_expr, p, m = witness
            x_sym = sympy.Symbol('x')
            if isinstance(f_expr, sympy.Poly):
                f = f_expr
            else:
                f = sympy.Poly(f_expr, x_sym)
            
            coeffs = f.all_coeffs()
            coeffs = [int(c) % m for c in coeffs]
            # Trim leading zeros
            while len(coeffs) > 1 and coeffs[0] == 0:
                coeffs.pop(0)
                
            n = len(coeffs) - 1
            h1 = bool(n >= 1)
            
            # In Z_m, p is a prime element iff p is a prime number and p divides m
            h2 = bool(sympy.isprime(p) and (m % p == 0) and (coeffs[0] % p != 0))
            
            h3 = bool(all(c % p == 0 for c in coeffs[1:]))
            h4 = bool(coeffs[-1] % (p**2) != 0)
            
            # neg_Q: f is reducible over K (which is Z_m since it's its own total ring of fractions)
            # A polynomial is reducible if it can be factored into two non-units.
            def is_unit(poly):
                if not poly: return False
                if math.gcd(poly[-1], m) != 1: return False
                for c in poly[:-1]:
                    is_nil = False
                    for pwr in range(1, m + 1):
                        if (c**pwr) % m == 0:
                            is_nil = True
                            break
                    if not is_nil: return False
                return True

            polys = []
            for deg in range(n + 1):
                for c in itertools.product(range(m), repeat=deg + 1):
                    if c[0] != 0 or deg == 0:
                        polys.append(list(c))
                        
            neg_q = False
            for g in polys:
                if is_unit(g): continue
                for h in polys:
                    if is_unit(h): continue
                    deg_g = len(g) - 1
                    deg_h = len(h) - 1
                    
                    # Heuristic degree bound to keep search fast
                    if deg_g + deg_h > n + 2:
                        continue
                    # Fast check on constant term
                    if (g[-1] * h[-1]) % m != coeffs[-1]:
                        continue
                    
                    prod = [0] * (deg_g + deg_h + 1)
                    for i in range(deg_g + 1):
                        for j in range(deg_h + 1):
                            prod[i+j] = (prod[i+j] + g[i] * h[j]) % m
                            
                    while len(prod) > 1 and prod[0] == 0:
                        prod.pop(0)
                        
                    if prod == coeffs:
                        neg_q = True
                        break
                if neg_q:
                    break
                    
            return [h1, h2, h3, h4, neg_q]
            
        elif len(witness) == 2:
            f_expr, p = witness
            x_sym = sympy.Symbol('x')
            if isinstance(f_expr, sympy.Poly):
                f = f_expr
            else:
                f = sympy.Poly(f_expr, x_sym, domain='ZZ')
            
            coeffs = [int(c) for c in f.all_coeffs()]
            n = len(coeffs) - 1
            h1 = bool(n >= 1)
            
            h2 = bool(sympy.isprime(p) and (coeffs[0] % p != 0))
            h3 = bool(all(c % p == 0 for c in coeffs[1:]))
            h4 = bool(coeffs[-1] % (p**2) != 0)
            
            # For ZZ, K is QQ
            neg_q = not sympy.polys.polytools.is_irreducible(f, domain='QQ')
            
            return [h1, h2, h3, h4, bool(neg_q)]
            
        else:
            return [False] * 5
            
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial of degree n >= 1",
    "H_2: p is a prime element and p does not divide a_n",
    "H_3: p divides a_i for all 0 <= i < n",
    "H_4: p^2 does not divide a_0",
    "¬Q: f(x) is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4