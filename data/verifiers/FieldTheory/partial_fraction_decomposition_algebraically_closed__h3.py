import sympy
from sympy import Symbol, fraction, cancel, degree

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Every rational function f(x) over an algebraically closed field K can be 
    uniquely written as a finite sum of terms of the form c / (x - a)^k."
    
    The dropped hypothesis is that f(x) must be a strictly proper rational function 
    (i.e., the degree of the numerator is strictly less than the degree of the denominator).
    """
    # H_1: K is an algebraically closed field
    # Since the witness is a SymPy expression, we can implicitly consider its coefficients 
    # to lie in an algebraically closed field (like the complex numbers).
    try:
        f = sympy.sympify(witness)
        h1 = True
    except Exception:
        h1 = False

    # H_2: f(x) is a rational function in the field of fractions K(x)
    try:
        h2 = bool(f.is_rational_function(x))
    except Exception:
        h2 = False

    # ¬Q: f(x) CANNOT be uniquely written as a finite sum of terms of the form c / (x - a)^k.
    # A rational function can be written as such a sum if and only if its polynomial part is zero,
    # which means it is strictly proper (degree of numerator < degree of denominator).
    # Therefore, the conclusion fails (¬Q is True) if degree of numerator >= degree of denominator.
    try:
        if not h2:
            neg_q = False
        else:
            f_canc = cancel(f)
            num, den = fraction(f_canc)
            if num == 0:
                # 0 is the empty sum, so it can be written in the required form.
                neg_q = False
            else:
                deg_num = degree(num, x)
                deg_den = degree(den, x)
                neg_q = bool(deg_num >= deg_den)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f(x) is a rational function in the field of fractions K(x)",
    "¬Q: f(x) cannot be uniquely written as a finite sum of terms of the form c / (x - a)^k"
]

N_HYP = 2
NEG_Q_INDEX = 2