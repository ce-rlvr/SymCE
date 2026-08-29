import sympy
from sympy import factorint

# Top-level setup
# No specific named objects needed for this Number Theory conjecture.

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the conjecture.
    The witness should be an integer n.
    """
    try:
        # H_1: The definition of P^1(Z/nZ) implicitly requires n to be an integer.
        h1_ok = isinstance(witness, (int, sympy.Integer))
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n = int(witness)
            
            # Calculate the true cardinality of P^1(Z/nZ)
            if n == 0:
                # For n=0, Z/0Z is isomorphic to Z. 
                # The pairs generating the unit ideal are coprime integers.
                # Modulo units (+1, -1), there are infinitely many equivalence classes.
                card = float('inf')
            else:
                n_abs = abs(n)
                if n_abs == 1:
                    card = 1
                else:
                    primes = factorint(n_abs).keys()
                    card = n_abs
                    for p in primes:
                        card = card * (p + 1) // p
            
            # Calculate the formula given in the conclusion: n * prod_{p|n} (1 + 1/p)
            if n == 0:
                # The product over prime divisors of 0 is infinite/undefined.
                form = None
            else:
                if n == 1 or n == -1:
                    form = n
                else:
                    primes = factorint(abs(n)).keys()
                    form = sympy.Rational(n, 1)
                    for p in primes:
                        form = form * sympy.Rational(p + 1, p)
            
            # neg_Q: The true cardinality does NOT equal the formula
            neg_q_ok = (card != form)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P^1(Z/nZ) is the set of equivalence classes of pairs (a,b) in (Z/nZ)^2 generating the unit ideal",
    "¬Q: The cardinality of P^1(Z/nZ) is not equal to n * prod_{p|n} (1 + 1/p)"
]

N_HYP = 1
NEG_Q_INDEX = 1