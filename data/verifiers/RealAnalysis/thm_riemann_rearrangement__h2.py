import sympy as sp
from sympy import Sum, oo, Symbol, Abs
import math

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Given a witness tuple (a_n, M), checks if it is a valid counterexample.
    a_n is the n-th term of the series, and M is the target limit.
    """
    if isinstance(witness, dict):
        a_n = witness.get('a_n')
        M = witness.get('M')
    else:
        try:
            a_n, M = witness
        except Exception:
            return [False, False]
            
    # H_1: \sum_{n=1}^\infty a_n is a conditionally convergent infinite series of real numbers
    h1 = False
    try:
        # Check if a_n is real for positive integers
        is_real_seq = True
        for i in range(1, 10):
            val = a_n.subs(n, i)
            if not val.is_real:
                is_real_seq = False
                break
        
        if is_real_seq:
            # Check convergence of the series
            sum_an = Sum(a_n, (n, 1, oo))
            if sum_an.is_convergent() is True:
                # Check divergence of the absolute series (conditional convergence)
                sum_abs_an = Sum(Abs(a_n), (n, 1, oo))
                if sum_abs_an.is_convergent() is False:
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist a permutation \sigma such that the rearranged series converges to M.
    # By the Riemann Rearrangement Theorem, a conditionally convergent real series can be rearranged 
    # to converge to any finite real number. Thus, a rearrangement converges to M if and only if 
    # M is a finite real number. The conclusion fails (neg_Q is True) iff M is NOT a finite real number.
    neg_q = False
    try:
        if hasattr(M, 'is_real') and hasattr(M, 'is_finite'):
            if M.is_real and M.is_finite:
                neg_q = False
            else:
                neg_q = True
        else:
            if isinstance(M, complex) and not isinstance(M, (int, float)):
                if M.imag != 0:
                    neg_q = True
                else:
                    neg_q = False
            elif isinstance(M, (int, float)):
                if math.isinf(M) or math.isnan(M):
                    neg_q = True
                else:
                    neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: \\sum_{n=1}^\\infty a_n is a conditionally convergent infinite series of real numbers",
    "¬Q: There does NOT exist a permutation \\sigma of the positive integers such that the rearranged series converges to M"
]

N_HYP = 1
NEG_Q_INDEX = 1