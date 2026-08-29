import sympy
from sympy import I, pi, exp, Rational, Integer, simplify, isprime
from sympy.abc import x, y, z

# Top-level setup
# No specific named bindings required for this field theory conjecture.

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should provide p, zeta_p, and g.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            zeta_p = witness.get('zeta_p')
            g = witness.get('g')
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 3:
                p, zeta_p, g = witness[:3]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: p is an odd prime number
    try:
        h1 = False
        if isinstance(p, (int, sympy.Integer)) or (hasattr(p, 'is_integer') and p.is_integer):
            p_val = int(p)
            if sympy.isprime(p_val) and p_val % 2 != 0:
                h1 = True
    except Exception:
        h1 = False

    # H2: zeta_p is a primitive p-th root of unity
    try:
        h2 = False
        if h1:
            # For a prime p, any p-th root of unity other than 1 is primitive.
            if sympy.simplify(zeta_p**p_val - 1) == 0 and sympy.simplify(zeta_p - 1) != 0:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The square of the Gauss sum g^2 is equal to (-1)^{(p-1)/2}p (must FAIL)
    try:
        neg_q = False
        if h1:
            expected = ((-1)**((p_val - 1) // 2)) * p_val
            if sympy.simplify(g**2 - expected) != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: zeta_p is a primitive p-th root of unity",
    "¬Q: g^2 is not equal to (-1)^{(p-1)/2}p"
]

N_HYP = 2
NEG_Q_INDEX = 2