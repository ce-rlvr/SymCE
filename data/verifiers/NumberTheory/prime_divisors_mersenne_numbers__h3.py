import sympy

# Top-level setup
# (No named bindings needed for number theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        p, q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is an odd prime
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False
        
    # H_2: q is a prime
    try:
        h2 = bool(sympy.isprime(q))
    except Exception:
        h2 = False
        
    # ¬Q: q ≢ 1 (mod 2p)
    try:
        neg_q = bool(q % (2 * p) != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: q is a prime",
    "¬Q: q is not congruent to 1 (mod 2p)"
]

N_HYP = 2
NEG_Q_INDEX = 2