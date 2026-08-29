import sympy
from sympy import Integer, Symbol, Expr
import math

# Top-level setup for witness expressions
x, y, z, t = sympy.symbols('x y z t')
I = sympy.I
sqrt = sympy.sqrt

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "¬Q: R is not integrally closed in K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_square(n):
    if n < 0:
        return False
    root = math.isqrt(int(n))
    return root * root == int(n)

def is_square_free(n):
    n = abs(int(n))
    if n == 0:
        return False
    if n == 1:
        return True
    for i in range(2, math.isqrt(n) + 1):
        if n % (i * i) == 0:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        # Case 1: Witness is a dictionary with "d" representing Z[sqrt(d)]
        if isinstance(witness, dict) and "d" in witness:
            d = int(witness["d"])
            if is_square(d):
                return [True, False]
            h1 = True
            neg_q = not (is_square_free(d) and (d % 4 != 1))
            return [h1, neg_q]
            
        # Case 2: Witness is an integer or string of integer representing Z[sqrt(d)]
        try:
            d = int(witness)
            if is_square(d):
                return [True, False]
            h1 = True
            neg_q = not (is_square_free(d) and (d % 4 != 1))
            return [h1, neg_q]
        except Exception:
            pass
            
        # Case 3: Witness is a string like "Z[sqrt(-3)]"
        if isinstance(witness, str):
            import re
            m = re.match(r'Z\[sqrt\(([-0-9]+)\)\]', witness.replace(' ', ''))
            if m:
                d = int(m.group(1))
                if is_square(d):
                    return [True, False]
                h1 = True
                neg_q = not (is_square_free(d) and (d % 4 != 1))
                return [h1, neg_q]
                
        # Case 4: Witness is a SymPy expression like sqrt(-3)
        if isinstance(witness, Expr):
            d_expr = witness**2
            if d_expr.is_Integer:
                d = int(d_expr)
                if is_square(d):
                    return [True, False]
                h1 = True
                neg_q = not (is_square_free(d) and (d % 4 != 1))
                return [h1, neg_q]
                
        # Case 5: Witness is an iterable of SymPy expressions (monomial generators for a polynomial subring)
        if isinstance(witness, (list, tuple, set)):
            gens = list(witness)
            if gens and all(isinstance(g, Expr) for g in gens):
                syms = set()
                for g in gens:
                    syms.update(g.free_symbols)
                if len(syms) == 1:
                    var = list(syms)[0]
                    from sympy import Poly
                    polys = []
                    is_valid_poly = True
                    for g in gens:
                        if not g.is_polynomial(var):
                            is_valid_poly = False
                            break
                        p = Poly(g, var)
                        # Ensure it is a monomial (exactly one term)
                        if len(p.terms()) != 1:
                            is_valid_poly = False
                            break
                        polys.append(p)
                        
                    if is_valid_poly:
                        degrees = [p.degree() for p in polys if p.degree() > 0]
                        if degrees:
                            gcd_deg = degrees[0]
                            for deg in degrees[1:]:
                                gcd_deg = math.gcd(gcd_deg, deg)
                            
                            h1 = True
                            neg_q = False
                            if gcd_deg > 0:
                                normalized_degrees = [d // gcd_deg for d in degrees]
                                # The integral closure of k[x^d1, ...] in its field of fractions is k[x^g] where g = gcd(d_i).
                                # It is integrally closed iff it equals k[x^g], which happens iff g is one of the generators.
                                if 1 not in normalized_degrees:
                                    neg_q = True
                            return [h1, neg_q]
                            
    except Exception:
        pass
        
    return [False, False]