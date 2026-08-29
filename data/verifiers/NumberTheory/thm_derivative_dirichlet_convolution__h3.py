import sympy
from sympy import divisors, log, simplify, expand_log

CONDITION_LABELS = [
    "H_1: f and g are arithmetic functions",
    "H_2: The derivative of an arithmetic function h is defined as h'(n) = h(n) \\log n",
    "¬Q: (f * g)' != f' * g + f * g'"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_arithmetic_func(func):
    return callable(func) or isinstance(func, (dict, list, tuple))

def eval_func(func, x):
    if callable(func):
        return func(x)
    elif isinstance(func, dict):
        return func.get(x, 0)
    elif isinstance(func, (list, tuple)):
        return func[x] if 0 <= x < len(func) else 0
    else:
        return 0

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, g, n = witness
                ns = [n]
            elif len(witness) == 2:
                f, g = witness
                ns = range(1, 21)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = is_arithmetic_func(f) and is_arithmetic_func(g)
    except Exception:
        h1 = False

    h2 = True

    try:
        neg_q = False
        for n in ns:
            try:
                if int(n) != n or n < 1:
                    continue
                n = int(n)
            except Exception:
                continue
            
            divs = divisors(n)
            
            # (f * g)(n)
            fg_n = sum(eval_func(f, d) * eval_func(g, n // d) for d in divs)
            lhs = fg_n * log(n)
            
            # (f' * g)(n)
            term1 = sum(eval_func(f, d) * log(d) * eval_func(g, n // d) for d in divs)
            
            # (f * g')(n)
            term2 = sum(eval_func(f, d) * eval_func(g, n // d) * log(n // d) for d in divs)
            
            rhs = term1 + term2
            
            diff = simplify(lhs - rhs)
            if diff != 0:
                diff = simplify(expand_log(diff, force=True))
                if diff != 0:
                    if diff.is_number:
                        try:
                            if abs(complex(diff)) > 1e-9:
                                neg_q = True
                                break
                        except Exception:
                            neg_q = True
                            break
                    else:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]