import sympy
from sympy import sympify

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        n = sympify(witness)
        # The witness must be a specific number, not a symbol or boolean
        if not n.is_number or isinstance(n, (bool, sympy.logic.boolalg.Boolean)):
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        # H_1: n is not congruent to 2 mod 4
        # For non-integers, n % 4 evaluates to a value that is not 2.
        mod_val = n % 4
        h1 = (mod_val != 2)
    except Exception:
        h1 = False
        
    try:
        # ¬Q: n cannot be written as x^2 - y^2 for integers x, y
        # An integer can be written as x^2 - y^2 iff it is not congruent to 2 mod 4.
        # A non-integer can never be written as x^2 - y^2 for integers x, y.
        if n.is_integer:
            neg_q = (int(n) % 4 == 2)
        else:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is not congruent to 2 mod 4",
    "¬Q: n cannot be written as the difference of two integer squares"
]

N_HYP = 1
NEG_Q_INDEX = 1