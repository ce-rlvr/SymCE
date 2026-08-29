import sympy
from sympy import sympify, isprime

# Top-level setup
# No specific named objects are needed for this fractional ideal approach.
# The verifier evaluates the conjecture in the ring of integers R = Z,
# where ideals are represented by their generators.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to provide generators for fractional ideals A and B,
    and a prime ideal P in the ring of integers Z.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('A', 0)
            b = witness.get('B', 0)
            p = witness.get('P', 0)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                a, b, p = witness
            elif len(witness) == 4:
                # Format (R, P, A, B)
                _, p, a, b = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        def extract_gen(x):
            if isinstance(x, (list, tuple, set)) and len(x) == 1:
                return list(x)[0]
            return x
            
        a = sympify(extract_gen(a))
        b = sympify(extract_gen(b))
        p = sympify(extract_gen(p))
        
        if p.is_number:
            p = abs(p)
            
        # H1: R is a commutative ring
        # We implicitly use R = Z, which is a commutative ring.
        h1 = True
        
        # H2: P is a prime ideal of R
        # In Z, the ideal (p) is prime iff p is a prime number.
        h2 = bool(isprime(p))
        
        # H3: The ideal product AB is contained in P
        # The ideal product of (a) and (b) is (a*b).
        # (a*b) is contained in (p) iff (a*b)/p is an integer.
        ab = a * b
        h3 = bool((ab / p).is_integer)
        
        # Q: A is contained in P or B is contained in P
        # A is contained in P iff a/p is an integer.
        a_in_p = bool((a / p).is_integer)
        b_in_p = bool((b / p).is_integer)
        
        # The conclusion fails if neither A nor B is contained in P.
        neg_q = not (a_in_p or b_in_p)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: The ideal product AB is contained in P",
    "¬Q: A is not contained in P and B is not contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3