import itertools
from sympy import S, Abs, sympify, continued_fraction_iterator, continued_fraction_convergents

def check_inequality(alpha, n):
    try:
        # Generate continued fraction terms up to a_{n+1}
        cf = list(itertools.islice(continued_fraction_iterator(alpha), n + 2))
        convergents = list(continued_fraction_convergents(cf))
        
        if len(convergents) <= n + 1:
            # If the continued fraction is finite and too short, we cannot check the bound.
            # Return True to avoid falsely flagging this as a counterexample.
            return True
            
        pn, qn = convergents[n].p, convergents[n].q
        pn1, qn1 = convergents[n+1].p, convergents[n+1].q
        
        error = Abs(alpha - convergents[n])
        lower_bound = S(1) / (qn * (qn1 + qn))
        upper_bound = S(1) / (qn * qn1)
        
        left_diff = error - lower_bound
        right_diff = upper_bound - error
        
        # Evaluate numerically with high precision to avoid float precision issues
        left_f = left_diff.evalf(500)
        right_f = right_diff.evalf(500)
        
        return left_f > 0 and right_f > 0
    except Exception:
        return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                alpha = sympify(witness[0])
                n = int(witness[1])
            else:
                alpha = sympify(witness[0])
                n = None
        else:
            alpha = sympify(witness)
            n = None
    except Exception:
        return [False, False, False]
        
    # H_1: alpha is an irrational number
    try:
        h1 = (alpha.is_irrational == True)
    except Exception:
        h1 = False
        
    # H_2: p_{n+1}/q_{n+1} is the (n+1)-th convergent of alpha
    # This implies n >= 0 is a valid index.
    try:
        if n is not None:
            h2 = (n >= 0)
        else:
            h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails at the witness
    try:
        if n is not None:
            neg_q = not check_inequality(alpha, n)
        else:
            neg_q = False
            # Search for an n where the inequality fails
            for i in range(50):
                if not check_inequality(alpha, i):
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an irrational number",
    "H_2: p_{n+1}/q_{n+1} is the (n+1)-th convergent of alpha",
    "not Q: The approximation error bounds fail for some n >= 0"
]

N_HYP = 2
NEG_Q_INDEX = 2