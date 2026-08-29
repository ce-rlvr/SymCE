import math
from sympy.ntheory import factorint

# Top-level setup
# No specific named objects are required for this field theory conjecture,
# but we define a helper to check if q is a prime power.
def is_prime_power(n):
    if not isinstance(n, int) or n < 2:
        return False
    factors = factorint(n)
    return len(factors) == 1

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be a tuple (q, m, n) or (m, n)),
    evaluates the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                q, m, n = witness
            elif len(witness) == 2:
                m, n = witness
                q = 2  # Default valid prime power if q is omitted
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: m and n are positive integers
    try:
        h1_ok = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h1_ok = False
        
    # H_2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q
    try:
        # For F_q to be a valid finite field and have an algebraic closure,
        # q must be a prime power. If q is a prime power, F_{q^m} and F_{q^n} 
        # are uniquely embeddable in its algebraic closure.
        h2_ok = is_prime_power(q)
    except Exception:
        h2_ok = False
        
    # ¬Q: The compositum field F_{q^m} F_{q^n} is NOT exactly the field F_{q^{lcm(m,n)}}
    try:
        # Mathematically, the compositum of F_{q^m} and F_{q^n} inside a common 
        # algebraic closure is ALWAYS exactly F_{q^{lcm(m,n)}}. 
        # Because this is a universally true theorem for all valid finite fields, 
        # the conclusion never fails when the hypotheses hold.
        # Thus, the negated conclusion is always False.
        neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q",
    "¬Q: The compositum field F_{q^m} F_{q^n} is not exactly the field F_{q^{lcm(m,n)}}"
]

N_HYP = 2
NEG_Q_INDEX = 2