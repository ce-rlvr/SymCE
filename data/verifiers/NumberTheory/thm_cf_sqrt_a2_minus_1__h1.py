import sympy

def conditions(witness) -> list[bool]:
    try:
        a = sympy.sympify(witness)
        h1 = bool(a >= 2)
    except Exception:
        h1 = False

    try:
        val = sympy.sqrt(a**2 - 1)
        it = sympy.continued_fraction_iterator(val)
        
        t0 = next(it)
        t1 = next(it)
        t2 = next(it)
        
        matches = (t0 == (a - 1)) and (t1 == 1) and (t2 == (2 * a - 2))
        neg_q = not matches
        
    except StopIteration:
        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: a >= 2", "¬Q: continued fraction does not match the pattern"]

N_HYP = 1
NEG_Q_INDEX = 1