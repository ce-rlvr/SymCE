import sympy
import math

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple (a, p)
        if len(witness) != 2:
            return [False, False, False]
        a, p = witness
        if not (isinstance(a, int) and isinstance(p, int)):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H2: q_p(a) = (a^{p-1}-1)/p is the Fermat quotient of a base p
    # This is a definition establishing notation, which holds for any integer base a and prime p.
    try:
        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The modular inverse of a modulo p^2 is congruent to a^{p-2}(1 - p \cdot q_p(a)) \pmod{p^2}
    # The conclusion fails if `a` has no modular inverse modulo p^2, or if it does but the formula gives a different result.
    try:
        if math.gcd(a, p**2) != 1:
            # Modular inverse does not exist, so the statement that it is congruent to the formula is false.
            neg_q = True
        else:
            # Modular inverse exists
            inv = pow(a, -1, p**2)
            
            # Evaluate the formula: a^{p-2} * (1 - p * q_p(a)) mod p^2
            # Note that p * q_p(a) = a^{p-1} - 1
            # So 1 - p * q_p(a) = 2 - a^{p-1}
            term1 = pow(a, p-2, p**2)
            term2 = (2 - pow(a, p-1, p**2)) % (p**2)
            formula_val = (term1 * term2) % (p**2)
            
            neg_q = bool(inv != formula_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: q_p(a) = (a^{p-1}-1)/p is the Fermat quotient of a base p",
    "¬Q: The modular inverse of a modulo p^2 is NOT congruent to a^{p-2}(1 - p \cdot q_p(a)) \pmod{p^2} (or does not exist)"
]

N_HYP = 2
NEG_Q_INDEX = 2