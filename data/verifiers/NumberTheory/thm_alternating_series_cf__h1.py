import sympy
from sympy import sympify
from sympy.ntheory import continued_fraction_iterator, continued_fraction_convergents

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - a_0, a_1, a_2... is the simple continued fraction expansion of alpha
      - p_n/q_n denotes the n-th convergent of alpha
    Conclusion:
      - alpha = a_0 + sum_{n=1}^infinity (-1)^{n-1} / (q_n q_{n-1})
    
    The dropped hypothesis is that alpha is irrational. For rational alpha, 
    the continued fraction is finite, making the infinite sum undefined, 
    so the equality fails.
    """
    try:
        alpha = sympify(witness)
    except Exception:
        return [False, False, False]

    # H_1: a_0, a_1, a_2... is the simple continued fraction expansion of alpha
    try:
        cf_iter = continued_fraction_iterator(alpha)
        a0 = next(cf_iter)
        h1 = True
    except Exception:
        h1 = False

    # H_2: p_n/q_n denotes the n-th convergent of alpha
    try:
        if h1:
            cf_iter = continued_fraction_iterator(alpha)
            convs = continued_fraction_convergents(cf_iter)
            next(convs)
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: alpha != a_0 + sum_{n=1}^infinity (-1)^{n-1} / (q_n q_{n-1})
    try:
        if not h1:
            neg_q = False
        else:
            cf_iter = continued_fraction_iterator(alpha)
            is_finite = False
            for i, _ in enumerate(cf_iter):
                # If we can compute more than 200 terms, we consider it infinite
                if i > 200:
                    break
            else:
                is_finite = True
            
            # If the continued fraction is finite (alpha is rational), the infinite sum 
            # is undefined because q_n does not exist for all n >= 1. 
            # Thus, the equality to alpha fails.
            if is_finite:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_0, a_1, a_2... is the simple continued fraction expansion of alpha",
    "H_2: p_n/q_n denotes the n-th convergent of alpha",
    "not Q: alpha != a_0 + sum_{n=1}^infinity (-1)^{n-1} / (q_n q_{n-1})"
]

N_HYP = 2
NEG_Q_INDEX = 2