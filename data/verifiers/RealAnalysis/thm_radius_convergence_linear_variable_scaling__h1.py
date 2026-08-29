import sympy
from sympy.abc import x

# Top-level setup: named object bindings that the witness expression may reference.
n = sympy.Symbol('n', integer=True, nonnegative=True)

def get_radius_of_convergence(a_n, n_sym):
    if a_n == 0:
        return sympy.oo
    
    # Try ratio test
    try:
        ratio = sympy.Abs(a_n / a_n.subs(n_sym, n_sym + 1))
        L = sympy.limit(ratio, n_sym, sympy.oo)
        if (L.is_number or L == sympy.oo) and L != sympy.nan:
            return L
    except Exception:
        pass
        
    # Try root test
    try:
        root = sympy.Abs(a_n)**(1 / n_sym)
        L = sympy.limit(root, n_sym, sympy.oo)
        if L == 0:
            return sympy.oo
        elif L == sympy.oo:
            return sympy.S(0)
        elif L.is_number and L != sympy.nan:
            return 1 / L
    except Exception:
        pass
        
    return None

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should provide (a_n, R, c) where:
      - a_n is the n-th coefficient of the power series (as a sympy expression in terms of n)
      - R is the claimed arbitrary radius of convergence (which makes the conjecture false)
      - c is the scaling factor
    """
    try:
        if isinstance(witness, dict):
            a_n = sympy.sympify(witness['a_n'])
            R = sympy.sympify(witness['R'])
            c = sympy.sympify(witness['c'])
        else:
            a_n, R, c = witness
            a_n = sympy.sympify(a_n)
            R = sympy.sympify(R)
            c = sympy.sympify(c)
    except Exception:
        return [False, False]
        
    # H_1: c is a non-zero real number
    try:
        c_val = complex(c)
        c_is_real = (c_val.imag == 0)
        c_nonzero = (abs(c_val) != 0)
        h1 = bool(c_is_real and c_nonzero)
    except Exception:
        h1 = False
        
    # ¬Q: The power series \sum a_n c^n x^n does NOT have a radius of convergence equal to R / |c|
    try:
        b_n = a_n * (c ** n)
        actual_R = get_radius_of_convergence(b_n, n)
        
        if actual_R is None:
            neg_q = False
        else:
            expected_R = R / sympy.Abs(c)
            
            if actual_R == sympy.oo and expected_R == sympy.oo:
                neg_q = False
            elif actual_R == sympy.oo or expected_R == sympy.oo:
                neg_q = True
            else:
                diff = sympy.simplify(actual_R - expected_R)
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: c is a non-zero real number",
    "¬Q: The power series sum a_n c^n x^n does NOT have a radius of convergence equal to R / |c|"
]

N_HYP = 1
NEG_Q_INDEX = 1