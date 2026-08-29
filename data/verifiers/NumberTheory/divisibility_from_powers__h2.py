import sympy

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            n = witness.get('n')
        else:
            a, b, n = witness
    except Exception:
        return [False, False, False]

    # H_1: a and b are positive integers
    try:
        h1 = (int(a) == a) and (int(b) == b) and (a > 0) and (b > 0)
    except Exception:
        h1 = False

    # H_2: a^n divides b^n
    try:
        try:
            n_val = float(n)
        except Exception:
            n_val = 0.0
            
        if abs(n_val) > 10000:
            h2 = False
        else:
            an = sympy.Rational(a, 1)**n
            bn = sympy.Rational(b, 1)**n
            
            an_is_int = False
            if isinstance(an, float):
                an_is_int = an.is_integer()
            elif hasattr(an, 'is_integer'):
                an_is_int = (an.is_integer is True)
            elif isinstance(an, int):
                an_is_int = True
                
            bn_is_int = False
            if isinstance(bn, float):
                bn_is_int = bn.is_integer()
            elif hasattr(bn, 'is_integer'):
                bn_is_int = (bn.is_integer is True)
            elif isinstance(bn, int):
                bn_is_int = True

            if not (an_is_int and bn_is_int):
                h2 = False
            elif an == 0:
                h2 = (bn == 0)
            else:
                ratio = bn / an
                if isinstance(ratio, float):
                    h2 = ratio.is_integer()
                elif hasattr(ratio, 'is_integer'):
                    h2 = (ratio.is_integer is True)
                elif isinstance(ratio, int):
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: a does not divide b
    try:
        neg_q = (b % a != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "H_2: a^n divides b^n",
    "¬Q: a does not divide b"
]

N_HYP = 2
NEG_Q_INDEX = 2