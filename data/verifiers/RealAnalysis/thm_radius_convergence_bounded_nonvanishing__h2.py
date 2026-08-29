import sympy
import math

# Define the symbol for the sequence index
n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a sequence a_n, provided as a callable or a sympy expression.
    """
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
            expr = sympy.sympify(expr)
            free_syms = expr.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                expr = expr.subs(sym, n)
            elif len(free_syms) > 1:
                return [False, False]
        expr = sympy.sympify(expr)
    except Exception:
        return [False, False]
        
    # H_1: {a_n} is a bounded sequence of real numbers
    h1_ok = False
    try:
        if expr.is_constant(n):
            if expr.is_number and expr.is_finite:
                h1_ok = True
        else:
            L = sympy.limit(sympy.Abs(expr), n, sympy.oo)
            is_bounded_limit = False
            if L == sympy.oo:
                is_bounded_limit = False
            elif isinstance(L, sympy.calculus.util.AccumBounds):
                is_bounded_limit = (L.max < sympy.oo)
            elif L.is_number and L < sympy.oo:
                is_bounded_limit = True
            
            if is_bounded_limit:
                # Check early terms to ensure no poles (e.g., 1/n at n=0)
                vals_ok = True
                for i in range(100):
                    val = expr.subs(n, i)
                    if val.is_number and not val.is_finite:
                        vals_ok = False
                        break
                if vals_ok:
                    h1_ok = True
    except Exception:
        pass

    # neg_Q: The radius of convergence of sum a_n x^n is NOT exactly 1
    neg_q_ok = False
    try:
        R = None
        
        # Try Root test first
        try:
            root = sympy.Abs(expr)**(1/n)
            L_root = sympy.limit(root, n, sympy.oo)
            if isinstance(L_root, sympy.calculus.util.AccumBounds):
                max_val = L_root.max
                if max_val == 0:
                    R = sympy.oo
                else:
                    R = 1 / max_val
            elif L_root.is_number:
                if L_root == 0:
                    R = sympy.oo
                else:
                    R = 1 / L_root
        except Exception:
            pass
            
        # Fallback to Ratio test
        if R is None:
            try:
                ratio = sympy.Abs(expr / expr.subs(n, n+1))
                L_ratio = sympy.limit(ratio, n, sympy.oo)
                if L_ratio.is_number:
                    R = L_ratio
            except Exception:
                pass
        
        if R is not None:
            if R != 1:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {a_n} is a bounded sequence of real numbers",
    "¬Q: The radius of convergence of sum a_n x^n is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1