import sympy
from sympy.ntheory import jacobi_symbol, is_primitive_root

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            a = witness['a']
            p = witness.get('p', 2**(2**n) + 1)
        else:
            n = witness[0]
            a = witness[1]
            p = witness[2] if len(witness) >= 3 else 2**(2**n) + 1
            
        # Prevent DoS from extremely large numbers
        if not (isinstance(n, (int, sympy.Integer)) and 0 <= n <= 6):
            return [False, False, False, False]
        if not (isinstance(p, (int, sympy.Integer)) and 0 < p <= 2**(2**6) + 1):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h2 = False

    try:
        h3 = jacobi_symbol(a, p) == -1
    except Exception:
        h3 = False

    try:
        neg_q = not is_primitive_root(a, p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a non-negative integer",
    "H_2: a is an integer",
    "H_3: Jacobi symbol (a/p) is -1",
    "¬Q: a is not a primitive root modulo p"
]

N_HYP = 3
NEG_Q_INDEX = 3