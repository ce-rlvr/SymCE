import sympy
import math

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the false conjecture.
    The witness can be a dictionary {'n': n, 'A': A}, a tuple (n, A), or just an integer n.
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            A = witness['A']
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            n, A = witness
        else:
            n = witness
            if not isinstance(n, bool) and float(n) == int(n):
                n_int = int(n)
                s = str(abs(n_int))
                A = sum((1 if i % 2 == 0 else -1) * int(char) for i, char in enumerate(reversed(s)))
            else:
                A = None
    except Exception:
        return [False, False]
    
    # H_1: A is the alternating sum of the decimal digits of n, starting with a positive sign for the units digit
    try:
        if isinstance(n, bool) or isinstance(A, bool):
            h1 = False
        elif float(n) != int(n) or float(A) != int(A):
            h1 = False
        else:
            n_int = int(n)
            A_int = int(A)
            s = str(abs(n_int))
            expected_A = sum((1 if i % 2 == 0 else -1) * int(char) for i, char in enumerate(reversed(s)))
            h1 = (A_int == expected_A)
    except Exception:
        h1 = False

    # ¬Q: n is not congruent to A mod 11
    try:
        if isinstance(n, bool) or isinstance(A, bool):
            neg_q = False
        elif float(n) != int(n) or float(A) != int(A):
            neg_q = False
        else:
            n_int = int(n)
            A_int = int(A)
            neg_q = (n_int % 11 != A_int % 11)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is the alternating sum of the decimal digits of n, starting with a positive sign for the units digit",
    "¬Q: n is not congruent to A mod 11"
]

N_HYP = 1
NEG_Q_INDEX = 1