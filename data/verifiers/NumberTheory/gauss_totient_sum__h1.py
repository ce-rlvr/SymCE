import sympy
from sympy.ntheory import divisors, totient

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            return [False]
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        
        n = int(witness)
        if n == 0:
            # For n = 0, the sum of totients of divisors is undefined, 
            # so the conclusion sum_{d|n} phi(d) = n fails.
            neg_q = True
        else:
            divs = divisors(n)
            s = sum(totient(d) for d in divs)
            neg_q = bool(s != n)
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sum_{d|n} phi(d) != n"
]

N_HYP = 0
NEG_Q_INDEX = 0