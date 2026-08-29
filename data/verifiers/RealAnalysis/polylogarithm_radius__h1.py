import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x')

def evaluate_R(a_n, n_sym):
    """
    Evaluates the radius of convergence R for the series sum(a_n * x^n).
    Returns R if successful, otherwise None.
    """
    # Try root test: R = 1 / limsup |a_n|^(1/n)
    try:
        term = sp.Abs(a_n)**(1/n_sym)
        L = sp.limit(term, n_sym, sp.oo)
        if not isinstance(L, sp.Limit) and not L.has(sp.Limit) and L is not sp.nan:
            if L == 0:
                return sp.oo
            elif L == sp.oo:
                return 0
            else:
                return 1 / L
    except Exception:
        pass

    # Try ratio test: R = lim |a_n / a_{n+1}|
    try:
        a_n1 = a_n.subs(n_sym, n_sym + 1)
        term = sp.Abs(a_n / a_n1)
        L = sp.limit(term, n_sym, sp.oo)
        if not isinstance(L, sp.Limit) and not L.has(sp.Limit) and L is not sp.nan:
            return L
    except Exception:
        pass

    return None

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is the exponent `s` in the polylogarithm-like series sum(1/n^s * x^n).
    """
    # H_1: The power series is defined as sum(1/n^s x^n)
    try:
        s = witness
        
        # A valid power series in x cannot have coefficients that depend on x
        if hasattr(s, 'free_symbols') and x in s.free_symbols:
            return [False, False]
            
        # Handle infinite cases explicitly
        if s == sp.oo or s == -sp.oo:
            return [True, True]
            
        a_n = 1 / n**s
        h1_ok = True
    except Exception:
        return [False, False]

    # ¬Q: The radius of convergence of the power series is not exactly 1
    try:
        R = evaluate_R(a_n, n)
        if R is not None and R is not sp.nan:
            # Check if R != 1 safely using sympy.simplify
            diff = sp.simplify(R - 1)
            neg_q_ok = bool(diff != 0)
        else:
            # If we cannot compute the limit, we cannot verify the counterexample
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The power series is defined as sum(1/n^s x^n)",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1