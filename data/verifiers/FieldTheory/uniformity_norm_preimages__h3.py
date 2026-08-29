import sympy
from sympy.ntheory import factorint

# Top-level setup
# No specific named objects required for this domain

def is_prime_power(q):
    if not isinstance(q, (int, sympy.Integer)) or q < 2:
        return False
    factors = factorint(q)
    return len(factors) == 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                q, n, c = witness
            elif len(witness) == 2:
                q, n = witness
                c = 0  # Default to the counterexample case (c = 0)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(is_prime_power(q))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isinstance(n, (int, sympy.Integer)) and n >= 1)
    except Exception:
        h2_ok = False

    try:
        # Determine if c represents the zero element in F_q
        is_zero = False
        if isinstance(c, (int, sympy.Integer)):
            factors = factorint(q)
            if factors:
                p = list(factors.keys())[0]
                if c % p == 0:
                    is_zero = True
        elif c == 0:
            is_zero = True
            
        # The norm map N_{F_{q^n}/F_q} is surjective onto F_q^*.
        # For c = 0, the only preimage is 0.
        # For c != 0, there are exactly (q^n - 1)/(q - 1) preimages.
        if is_zero:
            num_preimages = 1
        else:
            num_preimages = (q**n - 1) // (q - 1)
            
        expected = (q**n - 1) // (q - 1)
        
        # The conclusion FAILS if the actual number of preimages does not match the expected formula
        neg_q_ok = bool(num_preimages != expected)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^n} is a finite field extension of F_q of degree n",
    "¬Q: The number of preimages of c under the norm map is not exactly (q^n - 1)/(q - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2