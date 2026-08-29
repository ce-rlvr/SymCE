import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            a = witness['a']
            b = witness['b']
        else:
            n, a, b = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(a, int) or isinstance(a, sympy.Integer)) and \
             (isinstance(b, int) or isinstance(b, sympy.Integer))
    except Exception:
        h2 = False

    try:
        # The conclusion states that the congruence has a unique solution 
        # given by x = a^{-1}b (mod n).
        # This is true if and only if a and n are coprime (gcd(a, n) == 1).
        # If gcd(a, n) != 1, then a^{-1} does not exist modulo n, and the 
        # congruence either has no solutions or multiple solutions.
        # Thus, the conclusion fails (neg_Q is True) iff gcd(a, n) != 1.
        neg_q = sympy.gcd(a, n) != 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a and b are integers",
    "¬Q: The linear congruence does not have a unique solution given by x = a^{-1}b (mod n)"
]

N_HYP = 2
NEG_Q_INDEX = 2