import sympy
from sympy import sympify, simplify
from sympy.ntheory.continued_fraction import continued_fraction_iterator

# Top-level setup
# (No specific named objects required for this number theory problem)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: alpha is a real number",
    "H_2: n is an integer with n >= 1",
    "¬Q: alpha != (alpha_n * p_{n-1} + p_{n-2}) / (alpha_n * q_{n-1} + q_{n-2})"
]

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                alpha, n, alpha_n = witness
            elif len(witness) == 2:
                alpha, n = witness
                alpha_n = 0
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: alpha is a real number
    try:
        alpha_sym = sympify(alpha)
        h1 = (alpha_sym.is_real is True) or isinstance(alpha, (int, float))
    except Exception:
        h1 = False

    # H_2: n is an integer with n >= 1
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness
    try:
        it = continued_fraction_iterator(alpha_sym)
        a = []
        for _ in range(n):
            a.append(next(it))
            
        # Initial values for convergents
        p_prev2, q_prev2 = 0, 1  # p_{-2}, q_{-2}
        p_prev1, q_prev1 = 1, 0  # p_{-1}, q_{-1}
        
        for k in range(n):
            ak = a[k]
            pk = ak * p_prev1 + p_prev2
            qk = ak * q_prev1 + q_prev2
            p_prev2, q_prev2 = p_prev1, q_prev1
            p_prev1, q_prev1 = pk, qk
            
        p_n_minus_1, p_n_minus_2 = p_prev1, p_prev2
        q_n_minus_1, q_n_minus_2 = q_prev1, q_prev2
        
        alpha_n_sym = sympify(alpha_n)
        num = alpha_n_sym * p_n_minus_1 + p_n_minus_2
        den = alpha_n_sym * q_n_minus_1 + q_n_minus_2
        
        if den == 0:
            neg_q = True
        else:
            rhs = num / den
            diff = simplify(alpha_sym - rhs)
            neg_q = (diff != 0)
    except Exception:
        # If continued fraction computation fails (e.g. too short), 
        # or any other error occurs, we cannot evaluate the conclusion.
        neg_q = False

    return [h1, h2, neg_q]