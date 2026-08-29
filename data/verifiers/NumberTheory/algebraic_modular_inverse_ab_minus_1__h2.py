import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
        else:
            a, b = witness
    except Exception:
        return [False, False]

    try:
        h1 = False
        if isinstance(a, int):
            is_int = True
        elif hasattr(a, 'is_integer'):
            if callable(a.is_integer):
                is_int = a.is_integer()
            else:
                is_int = bool(a.is_integer)
        else:
            is_int = False
            
        if is_int and a > 1:
            h1 = True
    except Exception:
        h1 = False

    try:
        a_val = sympy.Rational(a)
        b_val = sympy.Rational(b)
        m = a_val * b_val - 1
        
        if not a_val.is_integer:
            neg_q = True
        elif m == 0:
            neg_q = True
        elif m.is_integer:
            m_int = int(m)
            try:
                # abs(m_int) is used to safely handle negative moduli in pow()
                inv = pow(int(a_val), -1, abs(m_int))
            except ValueError:
                # Modular inverse does not exist
                neg_q = True
            else:
                diff = sympy.Rational(inv) - b_val
                if (diff / m_int).is_integer:
                    neg_q = False
                else:
                    neg_q = True
        else:
            # Modulo is not an integer, standard modular arithmetic does not apply
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer strictly greater than 1",
    "¬Q: The modular inverse of a modulo ab-1 is NOT congruent to b (mod ab-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1