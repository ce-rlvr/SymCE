import sympy

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    
    The witness is expected to be an integer `n`.
    """
    # H_1: n is a positive integer
    try:
        h1 = (isinstance(witness, int) or isinstance(witness, sympy.Integer)) and not isinstance(witness, bool) and int(witness) > 0
    except Exception:
        h1 = False

    # H_2: \sigma(n) is the sum of divisors function (definition, trivially true for the context)
    h2 = True

    # H_3: \tau(n) is the number of divisors function (definition, trivially true for the context)
    h3 = True

    # ¬Q: \sum_{d|n} \phi(d) \sigma(n/d) != n \tau(n)
    try:
        if h1:
            n = int(witness)
            divs = sympy.divisors(n)
            
            # Calculate \sum_{d|n} \phi(d) \sigma(n/d)
            lhs = sum(sympy.totient(d) * sum(sympy.divisors(n // d)) for d in divs)
            
            # Calculate n \tau(n)
            rhs = n * len(divs)
            
            neg_q = bool(lhs != rhs)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: sigma(n) is the sum of divisors function",
    "H_3: tau(n) is the number of divisors function",
    "¬Q: sum_{d|n} phi(d) sigma(n/d) != n tau(n)"
]

N_HYP = 3
NEG_Q_INDEX = 3