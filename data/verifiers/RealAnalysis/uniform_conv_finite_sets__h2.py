import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        # Witness is expected to be a tuple: (S, f_n, f)
        # S: a finite iterable or sympy.Set of real numbers
        # f_n: a sympy expression representing the sequence of functions (using symbols x and n)
        # f: a sympy expression representing the limit function (using symbol x)
        S_obj, f_n, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: S is a finite subset of R
    h1_ok = False
    try:
        if isinstance(S_obj, (list, tuple, set)):
            h1_ok = all(sympy.sympify(elem).is_real for elem in S_obj)
        elif isinstance(S_obj, sympy.Set):
            if S_obj.is_finite:
                h1_ok = all(elem.is_real for elem in S_obj)
    except Exception:
        h1_ok = False

    # H_2: {f_n} converges pointwise to f on S
    h2_ok = False
    try:
        if isinstance(S_obj, (list, tuple, set)):
            elements = list(S_obj)
            is_finite = True
        elif isinstance(S_obj, sympy.Set) and S_obj.is_finite:
            elements = list(S_obj)
            is_finite = True
        else:
            is_finite = False
            
        if is_finite:
            h2_ok = True
            for s in elements:
                val_f_n = f_n.subs(x, s)
                val_f = f.subs(x, s)
                lim = sympy.limit(val_f_n, n, sympy.oo)
                if isinstance(lim, sympy.Limit) or lim != val_f:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # neg_Q: {f_n} does NOT converge uniformly to f on S
    neg_q_ok = False
    try:
        if is_finite:
            if not elements:
                # Uniform convergence holds vacuously on an empty set, so neg_Q is False
                neg_q_ok = False
            else:
                neg_q_ok = False
                for s in elements:
                    diff = f_n.subs(x, s) - f.subs(x, s)
                    lim = sympy.limit(diff, n, sympy.oo)
                    # If the limit of the difference is not 0, uniform convergence fails
                    if not isinstance(lim, sympy.Limit) and lim != 0:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: S is a finite subset of R",
    "H_2: {f_n} converges pointwise to a function f on S",
    "¬Q: The sequence {f_n} does not converge uniformly to f on S"
]

N_HYP = 2
NEG_Q_INDEX = 2