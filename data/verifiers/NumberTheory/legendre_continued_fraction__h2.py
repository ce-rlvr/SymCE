import sympy as sp
from sympy.ntheory.continued_fraction import continued_fraction_iterator

# Top-level setup
# No specific named objects needed for this number theory problem,
# but we can define some basics just in case.
I2 = sp.eye(2)
I3 = sp.eye(3)

def conditions(witness):
    try:
        # Witness is expected to be a tuple (x, p, q)
        if len(witness) != 3:
            return [False, False, False]
        x, p, q = witness
    except Exception:
        return [False, False, False]
        
    # H1: x is a real number
    try:
        x_sym = sp.sympify(x)
        h1 = x_sym.is_real
        if h1 is None:
            h1 = isinstance(x, (int, float, sp.Rational, sp.Float))
        h1 = bool(h1)
    except Exception:
        h1 = False

    # H2: |x - p/q| < 1/(2q^2)
    try:
        p_sym = sp.sympify(p)
        q_sym = sp.sympify(q)
        if q_sym == 0:
            h2 = False
        else:
            diff = sp.Abs(x_sym - p_sym / q_sym)
            bound = sp.Rational(1, 2) / (q_sym**2)
            if diff.is_number and bound.is_number:
                # Use evalf to safely compare without raising Relational errors
                h2 = bool((diff - bound).evalf() < 0)
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: p/q is NOT a convergent of the simple continued fraction expansion of x
    try:
        if q_sym == 0:
            neg_q = True
        else:
            convergents = []
            p_minus_1, q_minus_1 = 1, 0
            p_minus_2, q_minus_2 = 0, 1
            
            cf_iter = continued_fraction_iterator(x_sym)
            for i, a in enumerate(cf_iter):
                if i >= 1000:  # Limit to 1000 terms to ensure fast termination
                    break
                p_n = a * p_minus_1 + p_minus_2
                q_n = a * q_minus_1 + q_minus_2
                convergents.append((p_n, q_n))
                
                p_minus_2, q_minus_2 = p_minus_1, q_minus_1
                p_minus_1, q_minus_1 = p_n, q_n
                
            is_convergent = False
            for (cn_p, cn_q) in convergents:
                # A convergent is specifically the fraction (p_n, q_n) in lowest terms with q_n > 0
                if p_sym == cn_p and q_sym == cn_q:
                    is_convergent = True
                    break
            neg_q = not is_convergent
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number",
    "H_2: |x - p/q| < 1/(2q^2)",
    "¬Q: p/q is not a convergent of the simple continued fraction expansion of x"
]

N_HYP = 2
NEG_Q_INDEX = 2