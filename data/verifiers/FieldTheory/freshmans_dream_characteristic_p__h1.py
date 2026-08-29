import sympy
from sympy import sympify, simplify

# Top-level setup
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness.get('x', 1)
            y = witness.get('y', 1)
            p = witness.get('p', 2)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                x, y, p = witness
            elif len(witness) == 2:
                x, y = witness
                p = 2
            else:
                return [False, False]
        else:
            return [False, False]
            
        x = sympify(x)
        y = sympify(y)
        p = sympify(p)
        
        # H_1: x and y are elements of F
        h1 = True
        if p.is_integer is False:
            h1 = False
        if p.is_positive is False:
            h1 = False
        if getattr(x, 'is_commutative', None) is False:
            h1 = False
        if getattr(y, 'is_commutative', None) is False:
            h1 = False
            
        # neg_Q: (x+y)^p != x^p + y^p
        lhs = (x + y)**p
        rhs = x**p + y**p
        diff = simplify(lhs - rhs)
        
        if hasattr(diff, 'is_zero') and diff.is_zero is not None:
            neg_q = not diff.is_zero
        else:
            neg_q = bool(diff != 0)
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: x and y are elements of F",
    "¬Q: (x+y)^p != x^p + y^p"
]

N_HYP = 1
NEG_Q_INDEX = 1