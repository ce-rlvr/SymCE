import sympy as sp

# Top-level setup
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)
c = sp.Symbol('c', real=True)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and violates the conclusion.
    The witness is expected to be the sequence of coefficients a_n (as a sympy expression of n, 
    a callable, or a tuple where the first element is a_n).
    """
    try:
        if isinstance(witness, tuple):
            a_n = witness[0]
        elif callable(witness):
            a_n = witness(n)
        else:
            a_n = witness
            
        a_n = sp.sympify(a_n)
        
        # H_1: a_n is a valid sequence for a power series
        h1 = True
        try:
            if a_n.has(x):
                h1 = False
            val = a_n.subs(n, 1)
            if val.has(n):
                h1 = False
        except Exception:
            h1 = False
            
        # Helper to calculate the radius of convergence R
        def get_R(expr):
            # Try the ratio test
            try:
                ratio = sp.Abs(expr / expr.subs(n, n+1))
                L = sp.limit(ratio, n, sp.oo)
                if L.is_number or L == sp.oo:
                    return L
            except Exception:
                pass
            
            # Try the root test
            try:
                root = sp.Abs(expr)**(1/n)
                L = sp.limit(root, n, sp.oo)
                if L == 0:
                    return sp.oo
                elif L.is_number or L == sp.oo:
                    return 1 / L
            except Exception:
                pass
            
            return None

        # Calculate R for the original series and the differentiated series
        R = get_R(a_n)
        R_diff = get_R(n * a_n)
        
        # ¬Q: The differentiated series has a different radius of convergence
        if R is not None and R_diff is not None:
            if R == R_diff:
                neg_q = False
            else:
                diff = sp.simplify(R - R_diff)
                neg_q = bool(diff != 0)
        else:
            neg_q = False
            
    except Exception:
        h1 = False
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a_n is a valid sequence for a power series",
    "¬Q: The differentiated series has a different radius of convergence"
]

N_HYP = 1
NEG_Q_INDEX = 1