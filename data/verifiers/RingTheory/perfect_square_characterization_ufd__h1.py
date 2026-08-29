import sympy
import math

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        w = sympy.sympify(witness)
        
        # H_1: a is a non-zero, non-unit element in R
        # We evaluate this in Z or Z[x, y, z] where units are 1 and -1.
        if w == 0:
            h1 = False
        elif w in [1, -1]:
            h1 = False
        else:
            h1 = True
            
        if not h1:
            return [False, False]
            
        # Factor the expression to find its prime factorization and leading coefficient
        coeff, factors = sympy.factor_list(w)
        
        # We restrict our verification to rings like Z or Z[x] where the coefficient is an integer
        if not coeff.is_Integer:
            return [False, False]
            
        c = int(coeff)
        
        # Check if the coefficient is a perfect square in Z
        is_coeff_sq = (c >= 0) and (math.isqrt(c)**2 == c)
        
        # Check if every prime factor appears with an even exponent
        even_exp = all(exp % 2 == 0 for base, exp in factors)
        
        # The element is a perfect square in Z or Z[x] iff its unit/coefficient is a perfect square 
        # and all its prime factors have even exponents.
        is_sq = is_coeff_sq and even_exp
        
        # ¬Q: The biconditional fails (i.e., it is a perfect square XOR all prime factors have even exponents)
        neg_q = (is_sq != even_exp)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: a is a non-zero, non-unit element in R",
    "¬Q: The biconditional (a is a perfect square iff all prime factors have even exponents) is false"
]

N_HYP = 1
NEG_Q_INDEX = 1