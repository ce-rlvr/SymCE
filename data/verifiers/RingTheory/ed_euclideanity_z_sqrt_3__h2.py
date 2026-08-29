import sympy as sp

# Top-level setup
sqrt = sp.sqrt

def conditions(witness) -> list[bool]:
    try:
        a, b = None, None
        
        # Check if witness is provided as a tuple of integers (a, b)
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int) and isinstance(witness[1], int):
                a, b = witness
        else:
            # Check if witness is provided as a sympy expression a + b*sqrt(3)
            expr = sp.sympify(witness)
            expr = sp.expand(expr)
            
            # Extract a and b by substituting sqrt(3) with 0
            a_val = expr.subs(sp.sqrt(3), 0)
            b_val = sp.expand((expr - a_val) / sp.sqrt(3))
            
            a_is_int = getattr(a_val, 'is_Integer', False) or isinstance(a_val, int)
            b_is_int = getattr(b_val, 'is_Integer', False) or isinstance(b_val, int)
            
            if a_is_int and b_is_int:
                a, b = int(a_val), int(b_val)
                
        if a is not None and b is not None:
            h1 = True
            # The conclusion "R is a Euclidean domain with Euclidean function N" fails
            # because the algebraic norm N(a+b*sqrt(3)) = a^2 - 3b^2 can be negative,
            # violating the requirement that a Euclidean function maps to non-negative integers.
            neg_q = (a**2 - 3 * b**2 < 0)
            return [h1, neg_q]
            
    except Exception:
        pass
    
    return [False, False]

CONDITION_LABELS = [
    "H_1: witness is an element of Z adjoin sqrt(3)",
    "¬Q: N(witness) < 0, so the algebraic norm N is not a valid Euclidean function"
]

N_HYP = 1
NEG_Q_INDEX = 1