import sympy
import math

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: x is a real number such that x >= 2
    try:
        if isinstance(witness, complex) and witness.imag != 0:
            h1_ok = False
        else:
            h1_ok = float(witness) >= 2.0
    except Exception:
        h1_ok = False

    # ¬Q: \sum_{n \le x} \omega(n) \neq x \log \log x + O(x)
    try:
        x = witness
        limit = int(float(x))
        
        # Calculate \sum_{n \le x} \omega(n)
        # sympy.primefactors(n) returns a list of distinct prime factors of n.
        lhs = sum(len(sympy.primefactors(n)) for n in range(1, limit + 1))
        
        # Calculate x \log \log x + O(x)
        rhs = x * sympy.log(sympy.log(x)) + sympy.O(x)
        
        # The conclusion is an equality. We check if it fails (which it should for a numeric witness).
        neg_q_ok = not (lhs == rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is a real number such that x >= 2",
    "¬Q: sum_{n <= x} omega(n) != x log log x + O(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1