import math

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a and b are elements of R that are coprime",
    "H_3: x = a/b is a root of the polynomial f(x)",
    "¬Q: The element a does not divide c_0, or b does not divide the leading coefficient c_n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a dictionary or tuple providing:
      - a: integer
      - b: integer
      - coeffs: list of integers [c_0, c_1, ..., c_n] representing f(x) = sum(c_i * x^i)
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            coeffs = witness['coeffs']
        else:
            a, b, coeffs = witness
            
        a = int(a)
        b = int(b)
        coeffs = [int(c) for c in coeffs]
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a Unique Factorization Domain
    # By restricting the witness to integers, R = Z, which is a UFD.
    h1 = True
    
    # H_2: a and b are elements of R that are coprime
    try:
        h2 = math.gcd(a, b) == 1
    except Exception:
        h2 = False
        
    # H_3: x = a/b is a root of the polynomial f(x)
    try:
        if b == 0:
            h3 = False
        else:
            n = len(coeffs) - 1
            if n < 0:
                h3 = False
            else:
                # Evaluate f(a/b) = 0 by multiplying through by b^n to stay in integers
                val = sum(c * (a**i) * (b**(n - i)) for i, c in enumerate(coeffs))
                h3 = (val == 0)
    except Exception:
        h3 = False
        
    # ¬Q: The element a does not divide c_0, or b does not divide the leading coefficient c_n
    # Note: In any UFD, a|c_0 and b|c_n are always true. The only way the conclusion fails 
    # is if the dropped hypothesis (c_n != 0) is violated, meaning c_n is NOT the leading coefficient.
    try:
        if len(coeffs) == 0:
            neg_q = False
        else:
            c_0 = coeffs[0]
            c_n = coeffs[-1]
            
            a_divides_c0 = (c_0 % a == 0) if a != 0 else (c_0 == 0)
            b_divides_cn = (c_n % b == 0) if b != 0 else (c_n == 0)
            
            # If c_n == 0, then c_n is not the leading coefficient, making the statement 
            # "b divides the leading coefficient c_n" false.
            cn_is_lc = (c_n != 0)
            
            q = a_divides_c0 and b_divides_cn and cn_is_lc
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]