import sympy
from sympy import Symbol, limit, oo

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    The witness should be a dictionary with keys:
      'a_n': expression in terms of n (the sequence of coefficients)
      'c': center of the power series (real number)
      'R': the dropped hypothesis radius (real number or oo)
      'K': a tuple (k_min, k_max) representing the compact subset [k_min, k_max]
    """
    try:
        a_n = sympy.sympify(witness['a_n'])
        c = sympy.sympify(witness['c'])
        R = sympy.sympify(witness['R'])
        k_min, k_max = witness['K']
        k_min = sympy.sympify(k_min)
        k_max = sympy.sympify(k_max)
    except Exception:
        return [False, False, False]
        
    # H1: a_n is a valid expression for the sequence (only depends on n)
    try:
        if not a_n.free_symbols.issubset({n}):
            h1 = False
        else:
            a_n.subs(n, 1)
            h1 = True
    except Exception:
        h1 = False
        
    # H2: K is a compact subset of (c-R, c+R)
    # Since K is represented as [k_min, k_max], we check c - R < k_min <= k_max < c + R
    try:
        h2 = bool(c - R < k_min) and bool(k_min <= k_max) and bool(k_max < c + R)
    except Exception:
        h2 = False
        
    # Neg_Q: The power series does NOT converge uniformly on K
    # For a power series, it fails to converge uniformly on [k_min, k_max] iff 
    # it fails to converge pointwise at some point in the interval (e.g., the endpoints).
    neg_q = False
    try:
        term_max = a_n * (k_max - c)**n
        term_min = a_n * (k_min - c)**n
        
        # 1. Check if the n-th term fails to go to 0 at the endpoints
        try:
            lim_max = limit(sympy.Abs(term_max), n, oo)
            if lim_max != 0:
                neg_q = True
        except Exception:
            pass
            
        try:
            if not neg_q:
                lim_min = limit(sympy.Abs(term_min), n, oo)
                if lim_min != 0:
                    neg_q = True
        except Exception:
            pass

        # 2. Check if the endpoints are strictly outside the actual radius of convergence
        try:
            if not neg_q:
                a_n_plus_1 = a_n.subs(n, n + 1)
                R_actual = limit(sympy.Abs(a_n / a_n_plus_1), n, oo)
                dist_max = sympy.Abs(k_max - c)
                dist_min = sympy.Abs(k_min - c)
                
                if bool(dist_max > R_actual) or bool(dist_min > R_actual):
                    neg_q = True
        except Exception:
            pass
            
        # 3. Fallback to sympy's is_convergent for boundary cases
        try:
            if not neg_q:
                conv_max = sympy.Sum(term_max, (n, 1, oo)).is_convergent()
                if conv_max is sympy.false or conv_max == False:
                    neg_q = True
        except Exception:
            pass
            
        try:
            if not neg_q:
                conv_min = sympy.Sum(term_min, (n, 1, oo)).is_convergent()
                if conv_min is sympy.false or conv_min == False:
                    neg_q = True
        except Exception:
            pass

    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: sum a_n (x-c)^n is a power series",
    "H_2: K is a compact subset of the open interval (c-R, c+R)",
    "¬Q: The power series does NOT converge uniformly on K"
]

N_HYP = 2
NEG_Q_INDEX = 2