import sympy
import sympy.ntheory

# Top-level setup
# (No specific named bindings needed for this number theory problem)

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is an integer",
    "¬Q: The number of incongruent solutions modulo p to x^2 ≡ a (mod p) is not equal to 1 + (a/p) (or (a/p) is undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
        else:
            if len(witness) != 2:
                return [False, False, False]
            p, a = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(sympy.isprime(p) and p % 2 == 1)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool)
    except Exception:
        h2 = False
        
    try:
        # The conclusion is that the number of incongruent solutions modulo p
        # to x^2 = a (mod p) is 1 + (a/p).
        # In many classical texts, the Legendre symbol (a/p) is strictly defined 
        # only when p does not divide a. Dropping the hypothesis "p does not divide a" 
        # makes the expression 1 + (a/p) undefined for p | a, thus failing the conclusion.
        if a % p == 0:
            neg_q = True
        else:
            if p < 100000:
                sols = sum(1 for x in range(p) if (x*x - a) % p == 0)
                legendre = sympy.ntheory.legendre_symbol(a, p)
                neg_q = bool(sols != 1 + legendre)
            else:
                # For large p not dividing a, the theorem mathematically guarantees 1 + (a/p) solutions.
                neg_q = False
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]