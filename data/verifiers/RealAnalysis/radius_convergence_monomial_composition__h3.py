import sympy as sp
from sympy import limit, oo, Abs

# Top-level setup: named object bindings that the witness expression may reference
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x')

CONDITION_LABELS = [
    "H_1: sum a_n x^n is a power series with radius of convergence R",
    "H_2: R > 0",
    "¬Q: The power series sum a_n x^{kn} does not have a radius of convergence equal to R^{1/k}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_radius_of_convergence(a_n, n_sym):
    """Helper to compute the radius of convergence of sum a_n x^n."""
    # Try ratio test
    try:
        ratio = Abs(a_n / a_n.subs(n_sym, n_sym + 1))
        L = limit(ratio, n_sym, oo)
        if L == oo or (L.is_number and L.is_real and L is not sp.nan):
            return L
    except Exception:
        pass
    
    # Try root test
    try:
        root_val = Abs(a_n)**(1 / n_sym)
        L = limit(root_val, n_sym, oo)
        if L == 0:
            return oo
        elif L == oo:
            return sp.S(0)
        elif L.is_number and L.is_real and L is not sp.nan:
            return 1 / L
    except Exception:
        pass
    
    return None

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if len(witness) == 3:
            a_n, R, k = witness
        elif len(witness) == 2:
            a_n, k = witness
            if callable(a_n):
                a_n = a_n(n)
            a_n = sp.sympify(a_n)
            R = get_radius_of_convergence(a_n, n)
        else:
            return [False, False, False]
            
        if callable(a_n):
            a_n = a_n(n)
        a_n = sp.sympify(a_n)
        if R is not None:
            R = sp.sympify(R)
        k = sp.sympify(k)
    except Exception:
        return [False, False, False]

    # H_1: sum a_n x^n is a power series with radius of convergence R
    try:
        actual_R = get_radius_of_convergence(a_n, n)
        if actual_R is None or R is None:
            h1_ok = False
        else:
            if actual_R == oo and R == oo:
                h1_ok = True
            else:
                h1_ok = bool(sp.Eq(actual_R, R))
    except Exception:
        h1_ok = False

    # H_2: R > 0
    try:
        if R is None:
            h2_ok = False
        elif R == oo:
            h2_ok = True
        else:
            h2_ok = bool(R > 0)
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion fails at the witness
    try:
        is_ps = True
        # Check if the resulting series is a valid power series
        for i in range(1, 100):
            val = a_n.subs(n, i)
            if sp.simplify(val) != 0:
                ki = k * i
                try:
                    ki_float = float(ki)
                    if not (ki_float.is_integer() and ki_float >= 0):
                        is_ps = False
                        break
                except Exception:
                    is_ps = False
                    break
        
        if not is_ps:
            # If it's not a power series, the statement "The power series ... has radius ..." is false
            q = False
        else:
            try:
                k_float = float(k)
                if k_float == 0:
                    # R**(1/0) is undefined
                    q = False
                elif k_float < 0:
                    # If k < 0 and it's a power series, a_n must be 0 for all n > 0.
                    # The series is a constant, radius is oo. But R**(1/k) = oo**(negative) = 0.
                    q = False
                else:
                    # If k > 0 and it is a power series, the radius is exactly R**(1/k)
                    q = True
            except Exception:
                q = False
                
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]