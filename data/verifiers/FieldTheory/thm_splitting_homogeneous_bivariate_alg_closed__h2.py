import sympy
from sympy import symbols, Poly

x, y = symbols('x y')

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture.
    The conjecture claims that any polynomial over an algebraically closed field
    factors into a product of a non-zero constant and d linear homogeneous polynomials.
    (The dropped hypothesis is that F(x, y) is homogeneous of degree d).
    """
    # H_1: K is an algebraically closed field
    # We interpret the witness as a polynomial over C (which is algebraically closed).
    # We just need to verify that the witness is a valid polynomial in x and y.
    try:
        p = Poly(witness, x, y)
        h1 = True
    except Exception:
        h1 = False

    # neg_Q: F(x, y) does NOT factor into a product of a non-zero constant and d linear homogeneous polynomials
    # Over an algebraically closed field, a polynomial factors into linear homogeneous polynomials
    # if and only if it is homogeneous and non-zero.
    try:
        p = Poly(witness, x, y)
        if p.is_zero:
            neg_q = True
        else:
            neg_q = not p.is_homogeneous
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: F(x, y) does not factor into a product of a non-zero constant and d linear homogeneous polynomials"
]

N_HYP = 1
NEG_Q_INDEX = 1