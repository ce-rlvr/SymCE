import sympy
import math

# Top-level setup for potential witness expressions
Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.Symbol('R')
x = sympy.Symbol('x')
y = sympy.Symbol('y')

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 3:
                _, I, J = witness
            elif len(witness) == 2:
                I, J = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # Helper to unwrap single-element collections or parse strings
        def unwrap(val):
            if isinstance(val, (list, tuple, set)) and len(val) == 1:
                val = list(val)[0]
            if isinstance(val, str):
                try:
                    return int(val)
                except ValueError:
                    pass
                try:
                    return sympy.sympify(val)
                except Exception:
                    pass
            return val
            
        I = unwrap(I)
        J = unwrap(J)
        
        # H_1 and H_2: I and J are two-sided ideals of R.
        # In our implicit ring (e.g., Z or a polynomial ring), any element generates a two-sided ideal.
        h1 = True
        h2 = True
        
        # Check if I and J are actual ideal objects (e.g., from sympy.polys.rings)
        if hasattr(I, 'intersect') and hasattr(I, '__mul__'):
            try:
                prod = I * J
                cap = I.intersect(J)
                same_ideal = (prod == cap)
                return [h1, h2, not same_ideal]
            except Exception:
                pass
                
        # If I and J are integers, we treat them as generators of ideals in Z
        if isinstance(I, (int, sympy.Integer)) and isinstance(J, (int, sympy.Integer)):
            I_val = int(I)
            J_val = int(J)
            prod = I_val * J_val
            cap = math.lcm(I_val, J_val)
            same_ideal = abs(prod) == abs(cap)
            
        # Otherwise, treat them as generators in a polynomial ring
        else:
            prod = sympy.expand(I * J)
            cap = sympy.lcm(I, J)
            
            if prod == 0 and cap == 0:
                same_ideal = True
            elif cap == 0 or prod == 0:
                same_ideal = False
            else:
                ratio = sympy.cancel(prod / cap)
                same_ideal = ratio.is_constant()
                
        neg_q = not same_ideal
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "H_2: J is a two-sided ideal of R",
    "¬Q: IJ != I \\cap J"
]

N_HYP = 2
NEG_Q_INDEX = 2