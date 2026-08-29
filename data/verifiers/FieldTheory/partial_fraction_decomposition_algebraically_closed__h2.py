import sympy
from sympy import Symbol, simplify

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture states that any f(x) over an algebraically closed field K 
    with deg(numerator) < deg(denominator) can be uniquely written as a finite 
    sum of terms of the form c / (x - a)^k.
    
    The dropped hypothesis is that f(x) is non-zero. If f(x) = 0, it cannot be 
    written as a non-empty sum of such terms (assuming c != 0 for uniqueness), 
    or if c=0 is allowed, the representation is not unique.
    """
    
    # H_1: K is an algebraically closed field
    # We assume the witness is an expression over an algebraically closed field (e.g., C).
    # This is a property of the domain, so it holds for any valid expression witness.
    h1 = True
    
    # H_2: The degree of the numerator of f(x) is strictly less than the degree of the denominator of f(x)
    try:
        n, d = witness.as_numer_denom()
        if not n.is_polynomial(x) or not d.is_polynomial(x):
            h2 = False
        else:
            deg_n = sympy.degree(n, x)
            deg_d = sympy.degree(d, x)
            h2 = bool(deg_n < deg_d)
    except Exception:
        h2 = False
        
    # ¬Q: f(x) cannot be uniquely written as a finite sum of terms of the form c / (x - a)^k
    # For any non-zero proper rational function, the partial fraction decomposition exists and is unique.
    # For f(x) = 0, uniqueness or existence fails depending on the exact formalization of the sum.
    try:
        neg_q = bool(simplify(witness) == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: The degree of the numerator of f(x) is strictly less than the degree of the denominator of f(x)",
    "¬Q: f(x) cannot be uniquely written as a finite sum of terms of the form c / (x - a)^k"
]

N_HYP = 2
NEG_Q_INDEX = 2