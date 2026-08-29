import sympy
from sympy.ntheory import continued_fraction_iterator
import math

def conditions(witness):
    try:
        x, m = witness
    except Exception:
        return [False, False, False]
        
    # H1: x is a real number
    try:
        if isinstance(x, (int, float)):
            h1 = True
        else:
            x_sym = sympy.sympify(x)
            h1 = bool(x_sym.is_real)
    except Exception:
        h1 = False
        
    # H2: m is an integer
    try:
        if isinstance(m, int):
            h2 = True
        elif isinstance(m, float):
            h2 = m.is_integer()
        else:
            m_sym = sympy.sympify(m)
            h2 = bool(m_sym.is_integer)
    except Exception:
        h2 = False
        
    # neg_Q: The simple continued fraction expansion of x + m is NOT [a_0 + m; a_1, a_2, ...]
    # The notation implies an infinite continued fraction. If x is rational, its
    # continued fraction is finite, so the conclusion fails.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            x_sym = sympy.sympify(x)
            m_sym = sympy.sympify(m)
            val = x_sym + m_sym
            
            if x_sym.is_rational or isinstance(x, (int, float)):
                neg_q = True
            else:
                it_x = continued_fraction_iterator(x_sym)
                a0 = next(it_x)
                
                it_val = continued_fraction_iterator(val)
                val_a0 = next(it_val)
                
                if val_a0 != a0 + m_sym:
                    neg_q = True
                else:
                    neg_q = False
                    for _ in range(15):
                        try:
                            ax = next(it_x)
                            aval = next(it_val)
                            if ax != aval:
                                neg_q = True
                                break
                        except StopIteration:
                            break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number",
    "H_2: m is an integer",
    "neg_Q: The simple continued fraction expansion of x + m is not (a_0 + m; a_1, a_2, ...)"
]

N_HYP = 2
NEG_Q_INDEX = 2