import sympy
import math

# Top-level setup
# No specific named objects are required for this number theory conjecture.

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (n, S).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, S = witness
        else:
            n = witness
            S = None
            
        # Convert to int if it's exactly an integer to avoid spurious type errors
        if isinstance(n, (int, sympy.Integer)):
            n = int(n)
        else:
            try:
                if float(n).is_integer():
                    n = int(n)
            except Exception:
                pass
    except Exception:
        return [False, False, False]

    # H_1: n >= 2
    try:
        h1_ok = bool(n >= 2)
    except Exception:
        h1_ok = False

    # H_2: S is the set of all positive integers less than or equal to n that are coprime to n
    try:
        if S is None:
            h2_ok = False
        else:
            max_val = int(math.floor(float(n)))
            # Prevent hanging on unreasonably large witness values
            if max_val > 100000:
                h2_ok = False
            else:
                expected_S = set()
                for x in range(1, max_val + 1):
                    # Use sympy.gcd to safely handle potential non-integer n
                    if sympy.gcd(x, n) == 1:
                        expected_S.add(x)
                
                # Check if S matches the expected set
                h2_ok = (set(S) == expected_S)
    except Exception:
        h2_ok = False

    # Q: The sum of the squares of the elements in S is equal to the formula
    try:
        sum_sq = sum(x**2 for x in S)
        
        # Evaluate the formula components
        phi_n = sympy.totient(n)
        primes = sympy.primefactors(n)
        
        prod = 1
        for p in primes:
            prod *= (1 - p)
            
        # Use exact rational arithmetic to avoid floating point precision issues
        formula = sympy.Rational(n**2, 3) * phi_n + sympy.Rational(n, 6) * prod
        
        q_holds = (sum_sq == formula)
    except Exception:
        # If the formula cannot be evaluated (e.g., totient of a non-integer), the conclusion fails
        q_holds = False

    # neg_Q is True if the conclusion FAILS
    neg_q = not q_holds

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2",
    "H_2: S is the set of all positive integers less than or equal to n that are coprime to n",
    "not Q: The sum of the squares of the elements in S is NOT equal to the formula"
]

N_HYP = 2
NEG_Q_INDEX = 2