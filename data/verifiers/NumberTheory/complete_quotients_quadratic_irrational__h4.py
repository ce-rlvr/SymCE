import math

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "Form of Complete Quotients for Quadratic Irrationals"
    """
    try:
        d, P0, Q0 = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: d is a positive integer that is not a perfect square
    try:
        h1 = isinstance(d, int) and d > 0 and math.isqrt(d)**2 != d
    except Exception:
        h1 = False
        
    # H_2: alpha is a quadratic irrational, where P0 and Q0 are integers
    try:
        h2 = isinstance(P0, int) and isinstance(Q0, int) and Q0 != 0
    except Exception:
        h2 = False
        
    # H_3: Q0 divides d - P0^2
    try:
        h3 = Q0 != 0 and (d - P0**2) % Q0 == 0
    except Exception:
        h3 = False
        
    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: For all k >= 0, P_k and Q_k are integers, and Q_k divides d - P_k^2
    neg_q = False
    try:
        P = P0
        Q = Q0
        seen = set()
        fails = False
        
        # We compute the sequence of complete quotients.
        # Since quadratic irrationals have periodic continued fractions, 
        # the sequence of (P_k, Q_k) will eventually repeat.
        for k in range(1000):
            if not isinstance(P, int) or not isinstance(Q, int):
                fails = True
                break
            if Q == 0:
                fails = True
                break
            if (d - P**2) % Q != 0:
                fails = True
                break
            
            state = (P, Q)
            if state in seen:
                break
            seen.add(state)
            
            # Compute a_k = floor((P_k + sqrt(d)) / Q_k) using exact integer arithmetic
            isqrt_d = math.isqrt(d)
            if Q > 0:
                a = (P + isqrt_d) // Q
            else:
                # For negative Q, floor(-X / |Q|) = floor(floor(-X) / |Q|)
                # floor(-sqrt(d)) = -isqrt(d) - 1 since d is not a perfect square
                a = (-P - isqrt_d - 1) // abs(Q)
                
            P_next = a * Q - P
            Q_next = (d - P_next**2) // Q
            
            P, Q = P_next, Q_next
            
        neg_q = fails
    except Exception:
        # If any mathematical operation fails (e.g., division by zero), the conclusion fails
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: d is a positive integer that is not a perfect square",
    "H_2: alpha is a quadratic irrational, where P0 and Q0 are integers",
    "H_3: Q0 divides d - P0^2",
    "¬Q: The sequence of complete quotients fails to be integers or Q_k fails to divide d - P_k^2"
]

N_HYP = 3
NEG_Q_INDEX = 3