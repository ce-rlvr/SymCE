import sympy as sp

CONDITION_LABELS = [
    "H_1: sum a_n x^n is a power series with radius of convergence R",
    "not Q: The power series sum b_n x^n has a radius of convergence strictly less than min(R, 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The false conjecture dropped the definition of b_n (e.g., b_n = sum_{k=0}^n a_k),
    leaving b_n as a free variable. Thus, the witness must provide both a_n and b_n.
    
    Expected witness format: a tuple/list of two elements (a_n, b_n), or a dict 
    with keys 'a' and 'b', where the values are sympy expressions in terms of n, 
    constants, or callables.
    """
    try:
        if isinstance(witness, dict):
            a_obj = witness.get('a', witness.get('a_n'))
            b_obj = witness.get('b', witness.get('b_n'))
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            a_obj, b_obj = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    n_sym = sp.Symbol('n', integer=True, positive=True)

    def to_expr(obj):
        if hasattr(obj, 'free_symbols'):
            if len(obj.free_symbols) == 1:
                sym = list(obj.free_symbols)[0]
                return obj.subs(sym, n_sym)
            elif len(obj.free_symbols) == 0:
                return obj
        elif callable(obj):
            return obj(n_sym)
        return sp.sympify(obj)

    try:
        a_expr = to_expr(a_obj)
        b_expr = to_expr(b_obj)
    except Exception:
        return [False, False]

    def get_R(expr):
        if expr == 0:
            return sp.oo
        
        # Try Ratio test
        try:
            ratio = sp.simplify(expr / expr.subs(n_sym, n_sym + 1))
            R = sp.limit(sp.Abs(ratio), n_sym, sp.oo)
            if R == sp.oo or R.is_number:
                return R
        except Exception:
            pass
            
        # Try Root test
        try:
            root = sp.Abs(expr)**(1 / n_sym)
            L = sp.limit(root, n_sym, sp.oo)
            if L == 0:
                return sp.oo
            R = 1 / L
            if R == sp.oo or R.is_number:
                return R
        except Exception:
            pass
            
        raise ValueError("Could not compute radius of convergence")

    # Check Hypothesis 1: a_n is a power series with radius of convergence R
    try:
        R_a = get_R(a_expr)
        H1 = True
    except Exception:
        H1 = False
        R_a = None

    # Check Negated Conclusion: b_n has a radius of convergence strictly less than min(R, 1)
    try:
        if R_a is not None:
            R_b = get_R(b_expr)
            min_R_1 = sp.Min(R_a, 1)
            
            if R_b == sp.oo:
                neg_Q = False
            else:
                neg_Q = bool(R_b < min_R_1)
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, neg_Q]