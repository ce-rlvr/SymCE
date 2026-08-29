import sympy
from sympy import Rational, sqrt, N
from sympy.ntheory import continued_fraction_iterator, continued_fraction_convergents

def conditions(witness):
    # H_1: alpha is an irrational number
    try:
        h1_ok = (witness.is_irrational is True)
    except Exception:
        h1_ok = False

    # neg_Q: There are only finitely many rational numbers p/q such that |alpha - p/q| < 1/(sqrt(8)q^2)
    try:
        # Evaluate alpha to high precision to compute its continued fraction
        alpha_val = N(witness, 500)
        cf_iter = continued_fraction_iterator(alpha_val)
        
        partial_quotients = []
        for i, c in enumerate(cf_iter):
            if i > 80:
                break
            partial_quotients.append(c)
            
        # Generate the convergents from the partial quotients
        conv_iter = continued_fraction_convergents(partial_quotients)
        
        threshold = 1 / N(sqrt(8), 500)
        
        late_successes = 0
        # Check the convergents from index 40 to 80
        # For a valid counterexample (like the golden ratio), the limit of q^2 * |alpha - p/q| 
        # is 1/sqrt(5) > 1/sqrt(8), so eventually there will be 0 successes.
        for i, pq in enumerate(conv_iter):
            if i < 40:
                continue
            p, q = pq.numerator, pq.denominator
            val = q**2 * abs(alpha_val - Rational(p, q))
            if val < threshold:
                late_successes += 1
                
        neg_q_ok = (late_successes == 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: alpha is an irrational number",
    "¬Q: There are only finitely many rational numbers p/q such that |alpha - p/q| < 1/(sqrt(8)q^2)"
]

N_HYP = 1
NEG_Q_INDEX = 1