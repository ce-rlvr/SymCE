import sympy
from sympy import divisors

def eval_func(func, x):
    if callable(func):
        return func(x)
    elif isinstance(func, dict):
        return func[x]
    elif isinstance(func, (list, tuple)):
        return func[x]
    else:
        raise ValueError("Not a function")

def is_pos_int(x):
    try:
        if not isinstance(x, (int, sympy.Integer)):
            return False
        return int(x) == x and x > 0
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            epsilon = witness.get('epsilon', witness.get('\\epsilon', witness.get('eps')))
            n = witness.get('n')
        else:
            if len(witness) == 3:
                if is_pos_int(witness[2]):
                    f, epsilon, n = witness
                elif is_pos_int(witness[1]):
                    f, n, epsilon = witness
                elif is_pos_int(witness[0]):
                    n, f, epsilon = witness
                else:
                    f, epsilon, n = witness
            elif len(witness) == 2:
                f, n = witness
                epsilon = None
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: f is an arithmetic function
    try:
        _ = eval_func(f, 1)
        h1 = True
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = is_pos_int(n)
    except Exception:
        h2 = False

    # neg_Q: (f * \epsilon)(n) != f(n)
    try:
        if epsilon is None:
            neg_q = False
        else:
            n_int = int(n)
            conv = sum(eval_func(f, d) * eval_func(epsilon, n_int // d) for d in divisors(n_int))
            diff = conv - eval_func(f, n_int)
            if hasattr(diff, 'simplify'):
                neg_q = bool(sympy.simplify(diff) != 0)
            else:
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is an arithmetic function",
    "H_2: n is a positive integer",
    "¬Q: (f * \\epsilon)(n) != f(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2