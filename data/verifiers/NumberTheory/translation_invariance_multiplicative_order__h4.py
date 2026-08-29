import sympy
import sympy.ntheory

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (n, a, d, k).
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            d = witness.get('d')
            k = witness.get('k')
        else:
            n, a, d, k = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # H_2: a is an integer coprime to n
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and sympy.gcd(a, n) == 1
    except Exception:
        h2 = False

    # H_3: The multiplicative order of a modulo n is d
    try:
        if n == 1:
            h3 = (d == 1)
        else:
            h3 = (sympy.ntheory.n_order(a, n) == d)
    except Exception:
        h3 = False

    # ¬Q: The multiplicative order of a + kn modulo n is NOT equal to d
    try:
        val = a + k * n
        
        # Convert to int if it mathematically represents an integer
        try:
            if val == int(val):
                val = int(val)
        except Exception:
            pass

        if n == 1:
            if isinstance(val, (int, sympy.Integer)):
                q = (d == 1)
            else:
                q = False
        else:
            q = (sympy.ntheory.n_order(val, n) == d)
    except Exception:
        # If n_order raises an exception (e.g., val is not an integer or not coprime),
        # then the order is undefined, so it is not equal to d.
        q = False

    neg_q = not q

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a is an integer coprime to n",
    "H_3: The multiplicative order of a modulo n is d",
    "¬Q: The multiplicative order of a + kn modulo n is not equal to d"
]

N_HYP = 3
NEG_Q_INDEX = 3