import sympy as sp

# Top-level setup: named object bindings
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)
c = sp.Symbol('c', real=True)

def get_R(a_expr, n_sym):
    """
    Computes the radius of convergence R for the sequence a_n.
    Returns the radius as a SymPy expression, or None if it cannot be determined.
    """
    # Try the Ratio Test: R = lim_{n->oo} |a_n / a_{n+1}|
    try:
        ratio = sp.Abs(a_expr / a_expr.subs(n_sym, n_sym + 1)).simplify()
        L = sp.limit(ratio, n_sym, sp.oo)
        if L.is_number and not L.has(sp.nan) and not L.has(sp.zoo):
            return L
    except Exception:
        pass
    
    # Try the Root Test: R = 1 / lim_{n->oo} |a_n|^(1/n)
    try:
        root = sp.Abs(a_expr)**(1/n_sym)
        L = sp.limit(root, n_sym, sp.oo)
        if L == 0:
            return sp.oo
        elif L == sp.oo:
            return sp.S(0)
        elif L.is_number and not L.has(sp.nan) and not L.has(sp.zoo):
            return 1 / L
    except Exception:
        pass
    
    return None

def conditions(witness) -> list[bool]:
    n_sym = n
    try:
        # Extract the sequence expression from the witness
        if isinstance(witness, tuple):
            a_expr = witness[0]
        else:
            a_expr = witness
            
        if callable(a_expr):
            a_expr = sp.sympify(a_expr(n_sym))
        else:
            a_expr = sp.sympify(a_expr)
            
        # Verify it's a valid expression for a sequence
        if isinstance(a_expr, sp.Expr):
            free = a_expr.free_symbols
            if n_sym in free:
                pass
            elif len(free) == 1:
                n_sym = list(free)[0]
            elif len(free) == 0:
                pass
            else:
                # If there are multiple symbols and our default 'n' is not among them,
                # we cannot reliably determine the index variable.
                if n_sym not in free:
                    return [False, False]
        else:
            return [False, False]
            
        h1_ok = True
    except Exception:
        return [False, False]

    try:
        # Calculate radius of convergence for the original series
        R1 = get_R(a_expr, n_sym)
        
        # Calculate radius of convergence for the term-by-term integrated series
        R2 = get_R(a_expr / (n_sym + 1), n_sym)
        
        if R1 is None or R2 is None:
            neg_q = False
        else:
            # The conclusion states they have the EXACT SAME radius of convergence.
            # The negation of the conclusion is that they are DIFFERENT.
            if R1 == R2:
                neg_q = False
            else:
                diff = sp.simplify(R1 - R2)
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: a_n is a valid sequence for a power series",
    "¬Q: The integrated series does NOT have the exact same radius of convergence R"
]

N_HYP = 1
NEG_Q_INDEX = 1