import math
import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            k = witness.get('k')
        else:
            n, k = witness
    except Exception:
        return [False, False]

    # H1: n is an integer
    try:
        if isinstance(n, (int, sympy.Integer)):
            h1 = True
        elif hasattr(n, 'is_integer'):
            if callable(n.is_integer):
                h1 = bool(n.is_integer())
            else:
                h1 = bool(n.is_integer)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The product \prod_{i=0}^{k-1} (n+i) is NOT divisible by k!
    try:
        if isinstance(k, (int, sympy.Integer)):
            k_is_int = True
        elif hasattr(k, 'is_integer'):
            if callable(k.is_integer):
                k_is_int = bool(k.is_integer())
            else:
                k_is_int = bool(k.is_integer)
        else:
            k_is_int = False
            
        if not k_is_int:
            neg_q = True
        elif k < 0:
            neg_q = True
        else:
            k_int = int(k)
            if k_int > 10000:
                neg_q = False
            else:
                n_int = int(n)
                prod = 1
                for i in range(k_int):
                    prod *= (n_int + i)
                fact = math.factorial(k_int)
                neg_q = (prod % fact != 0)
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: The product is not divisible by k!"
]

N_HYP = 1
NEG_Q_INDEX = 1