import sympy
from sympy import symbols, cancel, degree
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = symbols('x y z')
x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

def conditions(witness):
    try:
        # Witness is expected to be a tuple (n, F_gens)
        # where n is the number of variables, F_gens is a list of rational functions generating F
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
            
        n, F_gens = witness
        
        if not isinstance(n, int) or n < 1:
            return [False, False, False]
            
        if not isinstance(F_gens, (list, tuple)):
            return [False, False, False]
            
        # H_1: K is a field
        h1 = True
        
        # H_2: E is the field of rational functions K(x_1, ..., x_n) in n independent variables
        h2 = True
        for f in F_gens:
            if not isinstance(f, sympy.Expr):
                h2 = False
                break
                
        # neg_Q: The degree of the field extension E over F is not exactly n!
        neg_q = False
        if h2:
            # We only support computing the degree if F_gens consists of n independent univariate rational functions
            if len(F_gens) == n:
                ext_deg = 1
                is_simple = True
                vars_used = set()
                for f in F_gens:
                    syms = f.free_symbols
                    if len(syms) == 0:
                        is_simple = False
                        break
                    elif len(syms) == 1:
                        s = list(syms)[0]
                        if s in vars_used:
                            is_simple = False
                            break
                        vars_used.add(s)
                        
                        f_canc = cancel(f)
                        num, den = f_canc.as_numer_denom()
                        
                        try:
                            deg_num = degree(num, s)
                        except Exception:
                            deg_num = 0
                            
                        try:
                            deg_den = degree(den, s)
                        except Exception:
                            deg_den = 0
                            
                        d = max(deg_num, deg_den)
                        if d == 0 or d == -sympy.oo:
                            is_simple = False
                            break
                        ext_deg *= d
                    else:
                        is_simple = False
                        break
                
                if is_simple:
                    if ext_deg != math.factorial(n):
                        neg_q = True

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: E is the field of rational functions K(x_1, ..., x_n) in n independent variables",
    "¬Q: The degree of the field extension E over F is not exactly n!"
]

N_HYP = 2
NEG_Q_INDEX = 2