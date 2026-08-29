import sympy
from sympy.ntheory import factorint, totient

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = isinstance(k, int) and k >= 1
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = isinstance(p, int) and p >= 1
    except Exception:
        h2_ok = False
        
    try:
        n = p**k
        if n > 10**6:
            neg_q_ok = False
        else:
            if n <= 2:
                actual_disc = 1
            else:
                phi = totient(n)
                factors = factorint(n)
                actual_disc = 1
                for q, e in factors.items():
                    exp_q = e * phi - phi // (q - 1)
                    actual_disc *= q**exp_q
                
            if p == 1:
                expected_disc = 1
            else:
                exponent = (p**(k-1)) * (p*k - k - 1)
                if exponent < 0:
                    expected_disc = sympy.Rational(1, p**(-exponent))
                else:
                    expected_disc = p**exponent
                    
            neg_q_ok = actual_disc != expected_disc
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "H_2: K is the p^k-th cyclotomic field (p is a positive integer)",
    "¬Q: The absolute discriminant is not equal to p^{p^{k-1}(pk-k-1)}"
]

N_HYP = 2
NEG_Q_INDEX = 2