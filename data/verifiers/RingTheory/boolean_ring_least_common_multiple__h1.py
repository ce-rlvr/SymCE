import sympy
from sympy import symbols
import math

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let a and b be elements of R. Then the product ab is a least common multiple of a and b in R."
    (The dropped hypothesis was that R is a Boolean ring).
    """
    try:
        # Extract a and b from the witness
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            if a is None or b is None:
                return [False, False]
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                _, a, b = witness
            elif len(witness) == 2:
                a, b = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        # H_1: a and b are elements of R
        # We accept integers or SymPy expressions as valid ring elements
        h1 = isinstance(a, (int, sympy.Integer, sympy.Expr)) and isinstance(b, (int, sympy.Integer, sympy.Expr))
        
        if not h1:
            return [False, False]
            
        # Evaluate whether ab is a least common multiple of a and b
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            a_val = int(a)
            b_val = int(b)
            if a_val == 0 and b_val == 0:
                is_lcm = True
            elif a_val == 0 or b_val == 0:
                is_lcm = True
            else:
                # In Z, ab is an LCM iff |ab| == lcm(a, b)
                actual_lcm = abs(a_val * b_val) // math.gcd(a_val, b_val)
                is_lcm = (abs(a_val * b_val) == actual_lcm)
        else:
            # For polynomials/expressions, ab is an LCM iff it divides the true LCM
            actual_lcm = sympy.lcm(a, b)
            ab = sympy.expand(a * b)
            _, r = sympy.div(actual_lcm, ab)
            is_lcm = (r == 0)
            
        # neg_Q: The product ab is NOT a least common multiple of a and b
        neg_q = not is_lcm
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "¬Q: The product ab is not a least common multiple of a and b in R"
]

N_HYP = 1
NEG_Q_INDEX = 1