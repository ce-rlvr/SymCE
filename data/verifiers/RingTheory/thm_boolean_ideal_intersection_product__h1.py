import sympy
import math
import re

# Top-level setup
Z = sympy.S.Integers

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "¬Q: The intersection I \\cap J is not equal to the product ideal IJ"
]

N_HYP = 1
NEG_Q_INDEX = 1

def _extract_ideal_gen(x):
    if isinstance(x, int):
        return abs(x)
    if hasattr(x, 'is_Integer') and x.is_Integer:
        return abs(int(x))
    s = str(x).replace(' ', '')
    match = re.search(r'-?\d+', s)
    if match:
        return abs(int(match.group()))
    if 'Z' in s or 'R' in s:
        return 1
    return abs(int(x))

def _get_n_m(witness):
    if isinstance(witness, dict):
        n = witness.get('I', witness.get('i', None))
        m = witness.get('J', witness.get('j', None))
        if n is None or m is None:
            vals = list(witness.values())
            if len(vals) >= 2:
                n, m = vals[0], vals[1]
            else:
                raise ValueError
        return n, m
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            return witness[0], witness[1]
        elif len(witness) == 3:
            return witness[1], witness[2]
        else:
            raise ValueError
    else:
        raise ValueError

def conditions(witness):
    """
    Evaluates the witness against the remaining hypotheses and the negated conclusion.
    We interpret the witness as representing two principal ideals nZ and mZ in the ring of integers Z.
    """
    try:
        n, m = _get_n_m(witness)
        n = _extract_ideal_gen(n)
        m = _extract_ideal_gen(m)
        # Any integer generates a valid ideal in Z
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        n, m = _get_n_m(witness)
        n = _extract_ideal_gen(n)
        m = _extract_ideal_gen(m)
        
        if n == 0 and m == 0:
            intersection_gen = 0
        else:
            intersection_gen = abs(n * m) // math.gcd(n, m)
            
        product_gen = abs(n * m)
        
        # The conclusion is I \cap J = IJ.
        # We want the negated conclusion: I \cap J != IJ.
        neg_q_ok = (intersection_gen != product_gen)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]