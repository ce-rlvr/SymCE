import sympy
from sympy import QQ, ZZ
from sympy.abc import x
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard integer rings Z_n as integers, and a helper Ideal class.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10

class Ideal:
    def __init__(self, *gens):
        self.gens = gens

def extract_gen(P):
    if hasattr(P, 'gens'):
        gens = P.gens
        if len(gens) == 1:
            return gens[0]
        elif all(isinstance(g, (int, sympy.Integer)) for g in gens):
            g = int(gens[0])
            for gen in gens[1:]:
                g = math.gcd(g, int(gen))
            return g
    elif hasattr(P, 'gen'):
        return P.gen
    return P

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, P, e = witness
        
        P_gen = extract_gen(P)
        
        # Case 1: R is an integer (representing Z/nZ or Z if n=0)
        if isinstance(R, (int, sympy.Integer)) and isinstance(P_gen, (int, sympy.Integer)) and isinstance(e, (int, sympy.Integer)):
            n = int(R)
            p = int(P_gen)
            e = int(e)
            
            h1 = (n >= 0)
            g = math.gcd(n, p)
            if g == 0:
                h2 = True
            else:
                h2 = sympy.isprime(g)
                
            if g == 0:
                e_in_P = (e == 0)
                one_minus_e_in_P = ((1 - e) == 0)
            else:
                e_in_P = (e % g == 0)
                one_minus_e_in_P = ((1 - e) % g == 0)
                
            exactly_one = (e_in_P != one_minus_e_in_P)
            neg_q = not exactly_one
            return [h1, h2, neg_q]
            
        # Case 2: R is sympy.ZZ
        if R == sympy.ZZ:
            if isinstance(P_gen, (int, sympy.Integer)) and isinstance(e, (int, sympy.Integer)):
                p = abs(int(P_gen))
                e = int(e)
                h1 = True
                h2 = (p == 0) or sympy.isprime(p)
                e_in_P = (e % p == 0) if p != 0 else (e == 0)
                one_minus_e_in_P = ((1 - e) % p == 0) if p != 0 else ((1 - e) == 0)
                exactly_one = (e_in_P != one_minus_e_in_P)
                neg_q = not exactly_one
                return [h1, h2, neg_q]
                
        # Case 2b: R is sympy.QQ
        if R == sympy.QQ:
            if isinstance(P_gen, (int, sympy.Integer)) and isinstance(e, (int, sympy.Integer, sympy.Rational)):
                p = abs(int(P_gen))
                h1 = True
                h2 = (p == 0)
                e_in_P = (e == 0) if p == 0 else True
                one_minus_e_in_P = ((1 - e) == 0) if p == 0 else True
                exactly_one = (e_in_P != one_minus_e_in_P)
                neg_q = not exactly_one
                return [h1, h2, neg_q]
                
        # Case 3: R is a polynomial ring (inferred from P_gen being an expression)
        if isinstance(P_gen, sympy.Expr):
            e_expr = sympy.sympify(e)
            h1 = True
            if P_gen == 0:
                h2 = True
                e_in_P = (sympy.simplify(e_expr) == 0)
                one_minus_e_in_P = (sympy.simplify(1 - e_expr) == 0)
            else:
                p_poly = sympy.Poly(P_gen, x, domain='QQ')
                h2 = p_poly.is_irreducible
                
                rem_e = sympy.rem(e_expr, P_gen, x)
                e_in_P = (sympy.simplify(rem_e) == 0)
                
                rem_1_minus_e = sympy.rem(1 - e_expr, P_gen, x)
                one_minus_e_in_P = (sympy.simplify(rem_1_minus_e) == 0)
                
            exactly_one = (e_in_P != one_minus_e_in_P)
            neg_q = not exactly_one
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal of R",
    "¬Q: It is not the case that exactly one of e or 1 - e belongs to P"
]

N_HYP = 2
NEG_Q_INDEX = 2