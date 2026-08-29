import sympy
from sympy.ntheory import totient, primefactors

# Top-level setup
# (No specific named objects needed for this number theory conjecture; integers are used directly)

def conditions(witness) -> list[bool]:
    try:
        # The witness must be an integer
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        n = int(witness)
        
        # Calculate the left-hand side: Euler's totient function
        lhs = totient(n)
        
        # Calculate the right-hand side: n * prod(1 - 1/p)
        factors = primefactors(n)
        rhs = sympy.Integer(n)
        for p in factors:
            rhs *= (1 - sympy.Rational(1, p))
            
        # The conclusion fails if LHS != RHS
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: phi(n) != n * prod_{p|n} (1 - 1/p)"
]

N_HYP = 0
NEG_Q_INDEX = 0