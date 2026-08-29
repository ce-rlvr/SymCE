import sympy

def conditions(witness) -> list[bool]:
    try:
        # The witness must be an integer.
        p = int(witness)
        if p != witness:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: Let p be a prime number.
    # The dropped hypothesis from the true theorem is that p is POSITIVE.
    # In ring theory, negative primes (e.g., -11) are also prime numbers.
    try:
        h1 = sympy.isprime(abs(p))
    except Exception:
        h1 = False
        
    # H_2: Let p = 1 (mod 5) or p = 4 (mod 5).
    try:
        mod5 = p % 5
        h2 = (mod5 == 1) or (mod5 == 4)
    except Exception:
        h2 = False
        
    # ¬Q: F_{p-1} != 0 (mod p)
    # The conclusion must FAIL at the witness.
    try:
        if p == 0:
            neg_q = False
        else:
            F = sympy.fibonacci(p - 1)
            neg_q = (F % p) != 0
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p = 1 (mod 5) or p = 4 (mod 5)",
    "¬Q: F_{p-1} != 0 (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2