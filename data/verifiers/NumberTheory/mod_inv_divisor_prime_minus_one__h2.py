import sympy
from sympy.ntheory import isprime
from sympy import sympify, Rational

# Top-level setup
# (No specific named objects needed for this NumberTheory conjecture; use integers/rationals directly)

def conditions(witness):
    try:
        p, a = witness
    except Exception:
        return [False, False, False]
        
    # H1: p is an odd prime
    try:
        h1 = isprime(p) and p % 2 == 1
    except Exception:
        h1 = False
        
    # H2: a divides p - 1
    try:
        p_sym = sympify(p)
        a_sym = sympify(a)
        if a_sym.is_Float:
            a_sym = Rational(a_sym)
            
        if a_sym == 0:
            h2 = False
        else:
            quotient = (p_sym - 1) / a_sym
            h2 = quotient.is_integer
    except Exception:
        h2 = False
        
    # neg_Q: The modular inverse of a modulo p is NOT congruent to p - (p-1)/a (mod p)
    try:
        p_sym = sympify(p)
        a_sym = sympify(a)
        if a_sym.is_Float:
            a_sym = Rational(a_sym)
            
        if a_sym == 0:
            neg_q = True
        else:
            quotient = (p_sym - 1) / a_sym
            
            if a_sym.is_integer:
                val_a = int(a_sym) % int(p_sym)
                inv_a = pow(val_a, -1, int(p_sym))
            elif a_sym.is_Rational:
                num, den = a_sym.as_numer_denom()
                inv_den = pow(int(den) % int(p_sym), -1, int(p_sym))
                val_a = (int(num) * inv_den) % int(p_sym)
                inv_a = pow(val_a, -1, int(p_sym))
            else:
                raise ValueError("Unsupported type for modular inverse")
                
            expected = p_sym - quotient
            if not expected.is_integer:
                neg_q = True
            else:
                q_holds = (inv_a - int(expected)) % int(p_sym) == 0
                neg_q = not q_holds
    except Exception:
        # If the modular inverse does not exist (e.g. denominator shares a factor with p),
        # or any other error occurs, the conclusion fails.
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a divides p - 1",
    "¬Q: The modular inverse of a modulo p is NOT congruent to p - (p-1)/a (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2