import sympy
from sympy.ntheory import divisor_sigma

# Top-level setup
# No specific named objects required for this Number Theory problem.

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False]
    
    # H_1: m is a proper divisor of n (m divides n and m < n)
    try:
        if not (isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer))):
            h1 = False
        else:
            m_int = int(m)
            n_int = int(n)
            if m_int == 0:
                h1 = (n_int == 0) and (m_int < n_int)
            else:
                h1 = (n_int % m_int == 0) and (m_int < n_int)
    except Exception:
        h1 = False
        
    # neg_Q: sigma(m)/m < sigma(n)/n FAILS
    try:
        m_int = int(m)
        n_int = int(n)
        sig_m = divisor_sigma(m_int)
        sig_n = divisor_sigma(n_int)
        val_m = sympy.Rational(sig_m, m_int)
        val_n = sympy.Rational(sig_n, n_int)
        q = bool(val_m < val_n)
    except Exception:
        # If evaluating the conclusion raises an error (e.g., division by zero or sigma(0)),
        # then the conclusion fails to hold.
        q = False
        
    neg_q = not q
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m is a proper divisor of n (m divides n and m < n)",
    "¬Q: The abundancy index strict monotonicity fails (sigma(m)/m < sigma(n)/n is false or undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1