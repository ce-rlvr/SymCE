import math
from sympy import sympify, Rational
from sympy.ntheory.continued_fraction import continued_fraction_iterator, continued_fraction_convergents

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    Hypotheses:
      - x is a real number
      - p and q are coprime integers
      - q > 0
    Conclusion:
      - p/q is a convergent of the simple continued fraction expansion of x
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        x, p, q = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: x is a real number
    try:
        x_sym = sympify(x)
        h1 = x_sym.is_real
        if h1 is None:
            h1 = isinstance(x, (int, float))
        h1 = bool(h1)
    except Exception:
        h1 = False

    # H_2: p and q are coprime integers
    try:
        p_val = int(p)
        q_val = int(q)
        h2 = (p == p_val) and (q == q_val) and (math.gcd(p_val, q_val) == 1)
    except Exception:
        h2 = False

    # H_3: q > 0
    try:
        q_val = int(q)
        h3 = (q == q_val) and (q_val > 0)
    except Exception:
        h3 = False

    # ¬Q: p/q is NOT a convergent of the simple continued fraction expansion of x
    try:
        target = Rational(p_val, q_val)
        cf_iter = continued_fraction_iterator(x_sym)
        cf = []
        for i, c in enumerate(cf_iter):
            cf.append(c)
            if i > 2000:
                break
        
        is_conv = False
        for c in continued_fraction_convergents(cf):
            if c == target:
                is_conv = True
                break
        neg_q = not is_conv
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number",
    "H_2: p and q are coprime integers",
    "H_3: q > 0",
    "¬Q: p/q is not a convergent of the simple continued fraction expansion of x"
]

N_HYP = 3
NEG_Q_INDEX = 3