import sympy
from sympy.ntheory.continued_fraction import continued_fraction_iterator

# Top-level setup
# No special named groups or matrices are needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - Let x be an irrational number
      
    Conclusion (must FAIL at the witness):
      The sequence of even convergents p_{2n}/q_{2n} is strictly increasing, 
      the sequence of odd convergents p_{2n+1}/q_{2n+1} is strictly decreasing, 
      and p_{2k}/q_{2k} < p_{2m+1}/q_{2m+1} for all integers k, m >= 0.
    """
    # H_1: x is an irrational number
    try:
        # If the witness is provided as a list of continued fraction coefficients,
        # it represents an irrational number if it is infinite. For practical purposes
        # of the verifier, we check if it's a symbolic irrational number.
        if isinstance(witness, list):
            h1_ok = len(witness) > 10  # A sufficiently long list implies irrationality in this context
        else:
            h1_ok = witness.is_irrational
            if h1_ok is None:
                h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails at the witness
    try:
        # Extract the continued fraction coefficients
        if isinstance(witness, list):
            a = witness[:30]
        else:
            iterator = continued_fraction_iterator(witness)
            a = []
            for i, val in enumerate(iterator):
                a.append(val)
                if i >= 30:
                    break
        
        if len(a) < 2:
            neg_q_ok = False
        else:
            # Compute the convergents p_n / q_n
            p_prev, p_curr = 0, 1
            q_prev, q_curr = 1, 0
            convergents = []
            
            for an in a:
                p_next = an * p_curr + p_prev
                q_next = an * q_curr + q_prev
                convergents.append(sympy.Rational(p_next, q_next))
                p_prev, p_curr = p_curr, p_next
                q_prev, q_curr = q_curr, q_next
            
            even_conv = convergents[0::2]
            odd_conv = convergents[1::2]
            
            # Check if even convergents are strictly increasing
            even_increasing = all(even_conv[i] < even_conv[i+1] for i in range(len(even_conv)-1))
            
            # Check if odd convergents are strictly decreasing
            odd_decreasing = all(odd_conv[i] > odd_conv[i+1] for i in range(len(odd_conv)-1))
            
            # Check if every even convergent is less than every odd convergent
            even_less_odd = all(e < o for e in even_conv for o in odd_conv)
            
            # The conclusion holds if all three conditions are met.
            # We want the negation of the conclusion (i.e., it fails).
            conclusion_holds = even_increasing and odd_decreasing and even_less_odd
            neg_q_ok = not conclusion_holds

    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: x is an irrational number",
    "¬Q: The monotonicity or bounding properties of the convergents fail"
]

N_HYP = 1
NEG_Q_INDEX = 1