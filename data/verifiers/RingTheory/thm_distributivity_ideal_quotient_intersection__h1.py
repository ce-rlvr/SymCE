import sympy
import math
from functools import reduce
from sympy import QQ, ZZ
from sympy.abc import x, y, z

# Helper for integer ideals
def _lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "The ideal quotient (\bigcap_{i=1}^n I_i : x) is equal to the intersection 
    of the ideal quotients \bigcap_{i=1}^n (I_i : x)."
    """
    try:
        if isinstance(witness, dict):
            I_list = witness.get('I_list', witness.get('ideals'))
            elem = witness.get('x', witness.get('element'))
            if I_list is None or elem is None:
                return [False, False, False]
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                I_list, elem = witness
            elif len(witness) == 3:
                _, I_list, elem = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: I_1, ..., I_n are ideals of R
    try:
        if not isinstance(I_list, (list, tuple)) or len(I_list) == 0:
            h1 = False
        else:
            h1 = True
            for I in I_list:
                # Accept integers (ideals in Z) or objects with intersect/quotient methods
                if not (isinstance(I, (int, sympy.Integer)) or (hasattr(I, 'intersect') and hasattr(I, 'quotient'))):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: x is an element of R
    try:
        if all(isinstance(I, (int, sympy.Integer)) for I in I_list):
            h2 = isinstance(elem, (int, sympy.Integer))
        else:
            h2 = hasattr(elem, 'ring') or hasattr(elem, 'parent') or hasattr(elem, 'as_expr') or isinstance(elem, (int, sympy.Integer))
    except Exception:
        h2 = False

    # ¬Q: (\bigcap I_i : x) != \bigcap (I_i : x)
    try:
        if all(isinstance(I, (int, sympy.Integer)) for I in I_list) and isinstance(elem, (int, sympy.Integer)):
            # Z case
            def z_intersect(lst):
                return reduce(_lcm, [abs(i) for i in lst])
            
            def z_quotient(I, e):
                I, e = abs(I), abs(e)
                if e == 0: return 1
                if I == 0: return 0
                return I // math.gcd(I, e)
            
            lhs_ideal = z_intersect(I_list)
            lhs = z_quotient(lhs_ideal, elem)
            
            rhs_ideals = [z_quotient(I, elem) for I in I_list]
            rhs = z_intersect(rhs_ideals)
            
            neg_q = (lhs != rhs)
        else:
            # General / Polynomial case
            def poly_intersect(lst):
                res = lst[0]
                for I in lst[1:]:
                    res = res.intersect(I)
                return res
            
            def poly_quotient(I, e):
                try:
                    if hasattr(I, 'ring') and hasattr(I.ring, 'ideal'):
                        return I.quotient(I.ring.ideal(e))
                except Exception:
                    pass
                return I.quotient(e)
                
            lhs_ideal = poly_intersect(I_list)
            lhs = poly_quotient(lhs_ideal, elem)
            
            rhs_ideals = [poly_quotient(I, elem) for I in I_list]
            rhs = poly_intersect(rhs_ideals)
            
            neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I_1, I_2, ..., I_n are ideals of R",
    "H_2: x is an element of R",
    "¬Q: The ideal quotient (\\bigcap_{i=1}^n I_i : x) is NOT equal to the intersection of the ideal quotients \\bigcap_{i=1}^n (I_i : x)"
]

N_HYP = 2
NEG_Q_INDEX = 2