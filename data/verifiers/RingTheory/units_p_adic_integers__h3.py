import sympy
from sympy import isprime
import fractions

# Top-level setup
# No specific named bindings are required for p-adic integers as witnesses 
# are typically provided as integers, fractions, or lists of coefficients.

def to_fraction(val):
    if isinstance(val, fractions.Fraction):
        return val
    if hasattr(val, 'p') and hasattr(val, 'q'):
        return fractions.Fraction(int(val.p), int(val.q))
    return fractions.Fraction(val)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            x = witness.get('x')
            a_0 = witness.get('a_0')
        elif hasattr(witness, 'p') and hasattr(witness, 'x'):
            p = witness.p
            x = witness.x
            a_0 = getattr(witness, 'a_0', None)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                p, x, a_0 = witness
            elif len(witness) == 2:
                p, x = witness
                a_0 = None
            else:
                p, x, a_0 = None, None, None
        else:
            p, x, a_0 = None, None, None
            
        if a_0 is None and isinstance(x, list) and len(x) > 0:
            a_0 = x[0]
    except Exception:
        p, x, a_0 = None, None, None

    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: x is in Z_p
    try:
        if isinstance(x, list):
            x_val = sum(c * (p**i) for i, c in enumerate(x))
        else:
            x_val = x
            
        f = to_fraction(x_val)
        h2 = bool(f.denominator % p != 0)
    except Exception:
        h2 = False

    # neg_Q: x is a unit in Z_p iff a_0 != 0 (we want this to FAIL, so XOR)
    try:
        if a_0 is None:
            raise ValueError("a_0 is not provided")
            
        if isinstance(x, list):
            x_val = sum(c * (p**i) for i, c in enumerate(x))
        else:
            x_val = x
            
        f = to_fraction(x_val)
        if f.denominator % p == 0:
            x_is_unit = False
        else:
            x_is_unit = bool(f.numerator % p != 0)
            
        a0_neq_0 = bool(a_0 != 0)
        
        neg_q = bool(x_is_unit != a0_neq_0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: x is an element of Z_p",
    "¬Q: (x is a unit in Z_p) is not equivalent to (a_0 != 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2