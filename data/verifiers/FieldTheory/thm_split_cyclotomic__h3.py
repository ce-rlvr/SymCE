import sympy
import sympy.polys

# Top-level setup
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: F is a field",
    "H_3: K is the splitting field of x^n - 1 over F",
    "¬Q: K is not F(zeta) for a primitive n-th root of unity zeta in K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            n = witness[0]
            F_obj = witness[1]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H_2: F is a field
    try:
        if isinstance(F_obj, int):
            h2 = sympy.isprime(F_obj)
            char = F_obj if h2 else 0
        elif isinstance(F_obj, str):
            if F_obj.startswith('F_'):
                p = int(F_obj[2:])
                h2 = sympy.isprime(p)
                char = p if h2 else 0
            elif F_obj in ['Q', 'R', 'C', 'QQ', 'RR', 'CC']:
                h2 = True
                char = 0
            else:
                h2 = False
                char = 0
        elif hasattr(F_obj, 'is_Field') and getattr(F_obj, 'is_Field'):
            h2 = True
            char = getattr(F_obj, 'characteristic', lambda: 0)()
        else:
            h2 = False
            char = 0
    except Exception:
        h2 = False
        char = 0

    # H_3: K is the splitting field of x^n - 1 over F
    # This is true by definition for any valid n and F.
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    # ¬Q: K is not F(zeta) for a primitive n-th root of unity zeta in K
    # This happens exactly when there is no primitive n-th root of unity in K,
    # which occurs if and only if the characteristic of F divides n.
    try:
        if h1 and h2:
            neg_q = bool(char > 0 and n % char == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]