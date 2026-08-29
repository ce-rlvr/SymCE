import sympy

# Top-level setup
# No specific named bindings are required for this number theory conjecture.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any real number x, the convergents p_n/q_n 
    of its continued fraction satisfy gcd(p_n, q_n) = 1 for all n >= 0.
    
    The missing hypothesis is that x must be an irrational number. 
    For rational numbers, the continued fraction is finite, so the sequence 
    of convergents is finite, making the condition "for all n >= 0" fail.
    """
    try:
        x = sympy.sympify(witness)
        h1 = bool(x.is_real)
    except Exception:
        h1 = False

    try:
        x = sympy.sympify(witness)
        it = sympy.continued_fraction_iterator(x)
        convs = sympy.continued_fraction_convergents(it)
        
        count = 0
        neg_q = False
        for c in convs:
            # c is a Rational or Integer, so c.p and c.q are its numerator and denominator.
            if sympy.gcd(c.p, c.q) != 1:
                neg_q = True
                break
            count += 1
            # If we can compute more than 100 convergents, we assume the sequence is infinite.
            if count > 100:
                break
        else:
            # The iterator was exhausted, meaning the sequence of convergents is finite.
            # Therefore, p_n and q_n do not exist for all n >= 0, and the conclusion fails.
            neg_q = True
            
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number",
    "¬Q: gcd(p_n, q_n) != 1 for some n >= 0, or the sequence of convergents is finite"
]

N_HYP = 1
NEG_Q_INDEX = 1