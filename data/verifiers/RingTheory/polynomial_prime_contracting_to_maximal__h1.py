import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Verifies that the witness is a valid counterexample to the conjecture.
    """
    try:
        # If witness is a dictionary of precomputed booleans
        if isinstance(witness, dict):
            return [
                bool(witness.get('h1', False)),
                bool(witness.get('h2', False)),
                bool(witness.get('h3', False)),
                bool(witness.get('neg_q', False))
            ]
            
        # If witness is an object with methods for each condition
        if hasattr(witness, 'h1') and callable(witness.h1):
            return [
                bool(witness.h1()),
                bool(witness.h2()),
                bool(witness.h3()),
                bool(witness.neg_q())
            ]
            
        # Otherwise, assume witness has R, M, P attributes with standard ideal methods
        R = witness.R
        M = witness.M
        P = witness.P
        
        try:
            h1 = bool(R.is_maximal_ideal(M))
        except Exception:
            h1 = False
            
        try:
            h2 = bool(P.is_prime_ideal())
        except Exception:
            h2 = False
            
        try:
            h3 = bool(P.intersection(R) == M)
        except Exception:
            h3 = False
            
        try:
            neg_q = bool((P != M.extend_to_poly()) and not P.is_maximal_ideal())
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: M is a maximal ideal of R",
    "H_2: P is a prime ideal of the polynomial ring over R",
    "H_3: The intersection of P and R is equal to M",
    "not Q: P is not M extended and P is not maximal"
]

N_HYP = 3
NEG_Q_INDEX = 3