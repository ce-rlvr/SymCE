import sympy
from sympy import symbols, Rational, Integer

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple containing the elements (a, b), 
    or potentially (R, a, b) or (R, d, a, b).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
            elif len(witness) == 3:
                _, a, b = witness
            elif len(witness) == 4:
                _, _, a, b = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: R is a Euclidean domain with d(xy) >= d(x) for non-zero x, y
    # We implicitly verify this by checking if a and b belong to a supported Euclidean domain:
    # either the integers Z, or a univariate polynomial ring over a field (e.g., Q[x]).
    try:
        is_int_a = isinstance(a, (int, sympy.Integer))
        is_int_b = isinstance(b, (int, sympy.Integer))
        
        if is_int_a and is_int_b:
            h1_ok = True
            # In Z, the standard Euclidean valuation is the absolute value
            d_func = lambda val: abs(int(val))
        else:
            def get_gens(val):
                if isinstance(val, (int, float, sympy.Number)):
                    return set()
                try:
                    p = sympy.poly(val)
                    return set(p.gens)
                except Exception:
                    return None

            gens_a = get_gens(a)
            gens_b = get_gens(b)
            
            if gens_a is not None and gens_b is not None:
                gens_union = gens_a.union(gens_b)
                # Must be at most univariate to be a Euclidean domain
                if len(gens_union) <= 1:
                    h1_ok = True
                    # In F[x], the standard Euclidean valuation is the degree of the polynomial
                    def d_func(val):
                        if isinstance(val, (int, float, sympy.Number)):
                            return 0
                        return sympy.poly(val).degree()
                else:
                    h1_ok = False
                    d_func = None
            else:
                h1_ok = False
                d_func = None
    except Exception:
        h1_ok = False
        d_func = None

    # H_2: a and b are non-zero elements of R
    try:
        if h1_ok:
            h2_ok = bool(a != 0) and bool(b != 0)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The Euclidean valuations are NOT equal, meaning d(a) != d(b)
    try:
        if h1_ok and h2_ok:
            neg_q_ok = bool(d_func(a) != d_func(b))
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain with d(xy) >= d(x) for non-zero x, y",
    "H_2: a and b are non-zero elements of R",
    "¬Q: d(a) != d(b)"
]

N_HYP = 2
NEG_Q_INDEX = 2