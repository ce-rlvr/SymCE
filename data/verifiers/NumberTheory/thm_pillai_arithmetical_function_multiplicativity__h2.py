import math
from sympy import divisors, totient

def conditions(witness):
    """
    Given a witness (m, n), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        # Witness should be a tuple or list of two elements
        if len(witness) != 2:
            return [False, False]
        m, n = witness
    except Exception:
        return [False, False]
        
    # Check Hypothesis 1: m and n are positive integers
    try:
        m_int = int(m)
        n_int = int(n)
        h1 = (m_int == m) and (n_int == n) and (m_int > 0) and (n_int > 0)
    except Exception:
        h1 = False
        
    # Check Negated Conclusion: P(mn) != P(m) * P(n)
    try:
        if h1:
            m_int = int(m)
            n_int = int(n)
            
            # Pillai's arithmetical function P(x) = sum_{k=1}^x gcd(k, x)
            # Can be efficiently computed as sum_{d|x} d * totient(x/d)
            def P(x):
                return sum(d * totient(x // d) for d in divisors(x))
                
            P_m = P(m_int)
            P_n = P(n_int)
            P_mn = P(m_int * n_int)
            
            neg_q = bool(P_mn != P_m * P_n)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: sum_{k=1}^{mn} gcd(k, mn) != (sum_{i=1}^m gcd(i, m)) * (sum_{j=1}^n gcd(j, n))"
]

N_HYP = 1
NEG_Q_INDEX = 1