import sympy
import itertools
import functools
import math

class Z2Ring:
    def __contains__(self, item):
        try:
            return int(item) in (0, 1)
        except Exception:
            return False
            
    def __str__(self):
        return "Z2"
        
    def __repr__(self):
        return "Z2"

# Top-level setup: define the standard Boolean ring Z2
Z2 = Z2Ring()

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If R is a Boolean ring and x is an element of R, then x^n = x."
    (The dropped hypothesis was n >= 1).
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', Z2)
            x = witness.get('x')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, x, n = witness
            elif len(witness) == 2:
                R = Z2
                x, n = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    if x is None or n is None:
        return [False, False, False]

    # H_1: R is a Boolean ring
    try:
        if isinstance(R, Z2Ring):
            h1 = True
        elif hasattr(R, 'order') and R.order == 2:
            h1 = True
        elif isinstance(R, (set, list, tuple)):
            try:
                h1 = set(int(a) for a in R) == {0, 1}
            except Exception:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: x is an element of R
    try:
        if isinstance(R, Z2Ring):
            h2 = x in R
        elif h1:
            h2 = int(x) in (0, 1)
        else:
            h2 = x in R
    except Exception:
        h2 = False

    # Ensure n is an integer
    try:
        n_int = int(n)
    except Exception:
        return [h1, h2, False]

    # ¬Q: x^n != x
    try:
        if h1 and h2:
            x_int = int(x)
            if n_int == 0:
                xn = 1
            elif n_int > 0:
                xn = x_int
                for _ in range(n_int - 1):
                    xn = (xn * x_int) % 2
            else:
                if x_int == 1:
                    xn = 1
                else:
                    raise ValueError("Undefined inverse")
            neg_q = bool(xn != x_int)
        else:
            if n_int == 0:
                xn = 1
            else:
                xn = x ** n_int
            neg_q = bool(xn != x)
    except Exception:
        # If evaluation fails (e.g., 0^-1), the equation x^n = x is undefined, hence False, so neg_Q is True.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: x is an element of R",
    "¬Q: x^n != x"
]

N_HYP = 2
NEG_Q_INDEX = 2