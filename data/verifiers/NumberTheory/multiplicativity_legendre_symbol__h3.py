import sympy
from sympy.ntheory import legendre_symbol

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
            b = witness.get('b')
        elif hasattr(witness, 'p') and hasattr(witness, 'a') and hasattr(witness, 'b'):
            p = witness.p
            a = witness.a
            b = witness.b
        else:
            p, a, b = witness
    except Exception:
        return [False, False, False]

    # Process p
    try:
        p_sym = sympy.S(p)
        if p_sym.is_integer:
            p_val = int(p_sym)
        else:
            p_val = p
        h1 = bool(sympy.isprime(p_val) and p_val % 2 != 0)
    except Exception:
        h1 = False
        p_val = p

    # Process a
    try:
        a_sym = sympy.S(a)
        h2 = bool(a_sym.is_integer)
        if h2:
            a_val = int(a_sym)
        else:
            a_val = a
    except Exception:
        h2 = False
        a_val = a

    # Process b
    try:
        b_sym = sympy.S(b)
        if b_sym.is_integer:
            b_val = int(b_sym)
        else:
            b_val = b
    except Exception:
        b_val = b

    # Evaluate negated conclusion
    try:
        ab = a_val * b_val
        ab_sym = sympy.S(ab)
        if ab_sym.is_integer:
            ab_val = int(ab_sym)
        else:
            ab_val = ab
            
        lhs = legendre_symbol(ab_val, p_val)
        rhs = legendre_symbol(a_val, p_val) * legendre_symbol(b_val, p_val)
        neg_q = bool(lhs != rhs)
    except Exception:
        # If legendre_symbol is undefined (e.g., due to non-integer arguments),
        # the conclusion fails to hold, so its negation is True.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is an integer",
    "¬Q: (ab/p) != (a/p)(b/p) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2