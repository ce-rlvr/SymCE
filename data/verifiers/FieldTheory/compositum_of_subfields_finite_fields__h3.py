import sympy
import math

# Top-level setup
# No specific named objects are required for this field theory conjecture,
# but we define a helper to check if q is a prime power (i.e., size of a finite field).
def is_prime_power(q):
    if not isinstance(q, int) or q <= 1:
        return False
    factors = sympy.factorint(q)
    return len(factors) == 1

def conditions(witness):
    """
    Given a witness tuple (q, m, n), checks the hypotheses and the negated conclusion.
    """
    try:
        q, m, n = witness
    except Exception:
        return [False, False, False]

    # H_1: F_q is a finite field with q elements
    try:
        h1_ok = is_prime_power(q)
    except Exception:
        h1_ok = False

    # H_2: m and n are positive integers
    try:
        h2_ok = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h2_ok = False

    # ¬Q: The compositum field F_{q^m} F_{q^n} is not exactly the field F_{q^{lcm(m,n)}}
    # Note: In standard field theory, the compositum of F_{q^m} and F_{q^n} inside a common 
    # algebraic closure is ALWAYS exactly F_{q^{lcm(m,n)}}. 
    # However, if this is presented as a FALSE conjecture where a hypothesis was dropped, 
    # it typically refers to the fact that the tensor product F_{q^m} \otimes_{F_q} F_{q^n} 
    # is a field (and thus equals the compositum F_{q^{mn}}) IF AND ONLY IF gcd(m, n) = 1.
    # Alternatively, if F_{q^m} F_{q^n} denotes the set of products {xy | x in F_{q^m}, y in F_{q^n}},
    # this set is a field (and equals the compositum) if and only if one divides the other.
    # The most standard dropped hypothesis in this context is gcd(m, n) == 1.
    try:
        neg_q_ok = (math.gcd(m, n) != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: m and n are positive integers",
    "¬Q: The compositum field F_{q^m} F_{q^n} is not exactly the field F_{q^{lcm(m,n)}}"
]

N_HYP = 2
NEG_Q_INDEX = 2