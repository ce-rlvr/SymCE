import sympy as sp
from sympy.ntheory import divisor_count

# Top-level setup
# No specific named objects needed for this number theory domain.

CONDITION_LABELS = [
    "H_1: s is a complex number such that Re(s) > 1",
    "H_2: d(n) denotes the number of positive divisors of n",
    "¬Q: \\sum_{n=1}^\\infty \\frac{d(n)}{n^s} \\neq \\zeta(s)^2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    neg_q = False
    
    if isinstance(witness, tuple) and len(witness) == 2:
        s, d = witness
    else:
        s = witness
        d = divisor_count
        
    # H_1: s is a complex number such that Re(s) > 1
    try:
        s_val = sp.sympify(s)
        if s_val.is_number and s_val.is_finite:
            re_s = sp.re(s_val)
            if bool(re_s > 1):
                h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: d(n) denotes the number of positive divisors of n
    try:
        is_div_func = True
        for n in [1, 2, 3, 4, 5, 6, 10, 12, 15, 16]:
            if d(n) != divisor_count(n):
                is_div_func = False
                break
        h2_ok = is_div_func
    except Exception:
        h2_ok = False
        
    # ¬Q: \sum_{n=1}^\infty \frac{d(n)}{n^s} != \zeta(s)^2
    try:
        s_val = sp.sympify(s)
        if not (s_val.is_number and s_val.is_finite):
            neg_q = True
        else:
            re_s = sp.re(s_val)
            if bool(re_s <= 1):
                # If Re(s) <= 1, the sum diverges and does not equal zeta(s)^2
                neg_q = True
            else:
                # For Re(s) > 1, the Dirichlet series equals zeta(s)^2 if and only if 
                # its coefficients match the divisor function exactly.
                series_match = True
                for n in range(1, 100):
                    if d(n) != divisor_count(n):
                        series_match = False
                        break
                neg_q = not series_match
    except Exception:
        neg_q = True
        
    return [h1_ok, h2_ok, neg_q]