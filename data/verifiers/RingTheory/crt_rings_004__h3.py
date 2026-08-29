import sympy
import math
from functools import reduce

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        # Parse witness: can be a tuple (ring, ideals) or just a list of ideals
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, ideals = witness
        else:
            ideals = witness
            
        if not isinstance(ideals, (list, tuple)):
            return [False, False, False]
            
        if len(ideals) < 1:
            return [False, False, False]
            
        # Check if all ideals are represented by integer generators (implies R = Z)
        is_int_list = True
        for val in ideals:
            if not isinstance(val, (int, sympy.Integer)):
                is_int_list = False
                break
                
        if is_int_list:
            h1 = True
            h2 = True
            
            def compute_lcm(a, b):
                if a == 0 and b == 0: return 0
                return abs(a * b) // math.gcd(a, b)
                
            int_gen = reduce(compute_lcm, [int(val) for val in ideals])
            prod_gen = reduce(lambda a, b: a * b, [int(val) for val in ideals])
            
            # In Z, two ideals are equal iff their generators have the same absolute value
            neg_q = abs(int_gen) != abs(prod_gen)
            return [h1, h2, neg_q]
            
        # Check if all ideals are represented by polynomial generators (implies R = k[x])
        try:
            expr_ideals = [sympy.sympify(val) for val in ideals]
            if all(isinstance(val, sympy.Expr) for val in expr_ideals):
                h1 = True
                h2 = True
                
                int_gen = reduce(sympy.lcm, expr_ideals)
                prod_gen = reduce(lambda a, b: a * b, expr_ideals)
                
                if prod_gen == 0:
                    neg_q = (int_gen != 0)
                else:
                    ratio = sympy.simplify(int_gen / prod_gen)
                    # In a polynomial ring over a field, two ideals are equal iff 
                    # their generators differ by a non-zero constant unit.
                    neg_q = not ratio.is_constant()
                    
                return [h1, h2, neg_q]
        except Exception:
            pass
            
        return [False, False, False]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I_1, I_2, ..., I_n are ideals of R",
    "¬Q: The intersection of the ideals is not equal to their product"
]

N_HYP = 2
NEG_Q_INDEX = 2