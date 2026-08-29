import sympy
import sympy.ntheory

def conditions(witness):
    try:
        a, b, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is an odd prime
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False
        
    # H_2: b is an integer
    try:
        if isinstance(b, (int, sympy.Integer)):
            h2 = True
        elif hasattr(b, 'is_integer') and b.is_integer:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: a \equiv b \pmod p
    try:
        h3 = bool((a - b) % p == 0)
    except Exception:
        h3 = False
        
    # neg_Q: The Legendre symbol (a/p) is equal to the Legendre symbol (b/p)
    try:
        val_a = sympy.ntheory.legendre_symbol(a, p)
        val_b = sympy.ntheory.legendre_symbol(b, p)
        neg_q = bool(val_a != val_b)
    except Exception:
        # If legendre_symbol is undefined for a (e.g., a is a float), the conclusion fails.
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: b is an integer",
    "H_3: a \\equiv b \\pmod p",
    "¬Q: The Legendre symbol (a/p) is not equal to (b/p) or is undefined"
]

N_HYP = 3
NEG_Q_INDEX = 3