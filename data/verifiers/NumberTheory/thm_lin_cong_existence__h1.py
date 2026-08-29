import math

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a tuple (a, b, m) or (a, b, m, d).
    """
    try:
        if len(witness) == 3:
            a, b, m = witness
            a, b, m = int(a), int(b), int(m)
            d = math.gcd(a, m)
            h1 = True
        elif len(witness) == 4:
            a, b, m, d_wit = witness
            a, b, m, d_wit = int(a), int(b), int(m), int(d_wit)
            d = math.gcd(a, m)
            h1 = (d_wit == d)
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # Check if d divides b
    try:
        if d == 0:
            d_divides_b = (b == 0)
        else:
            d_divides_b = (b % d == 0)
    except Exception:
        d_divides_b = False
        
    # Check if ax ≡ b (mod m) has a solution
    has_solution = False
    try:
        if m == 0:
            # Congruence modulo 0 is undefined in standard number theory,
            # so the statement "has a solution" is considered False.
            has_solution = False
        else:
            # For m != 0, Bezout's identity guarantees a solution iff d|b.
            # We check it explicitly for small m to be rigorous, 
            # and fall back to the mathematical fact for huge m to prevent timeouts.
            if abs(m) <= 1000:
                for x in range(-abs(m)-1, abs(m)+2):
                    if (a * x - b) % m == 0:
                        has_solution = True
                        break
            else:
                has_solution = d_divides_b
    except Exception:
        has_solution = False
        
    # Evaluate negated conclusion
    try:
        # The conclusion is: has_solution iff d_divides_b
        # The negated conclusion is that this equivalence fails.
        neg_q = (has_solution != d_divides_b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is defined as gcd(a, m)",
    "¬Q: The equivalence (ax ≡ b (mod m) has a solution iff d divides b) does not hold"
]

N_HYP = 1
NEG_Q_INDEX = 1