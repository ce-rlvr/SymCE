import sympy
from sympy.abc import x, y

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let K be an algebraically closed field. The equation f(x, y) = 0 has infinitely many distinct solutions in K x K."
    
    The dropped hypothesis was that f(x, y) is a non-constant polynomial.
    A valid counterexample is a non-zero constant polynomial, which has 0 (finitely many) solutions.
    """
    try:
        # Convert witness to a sympy expression
        witness = sympy.sympify(witness)
        
        # H_1: K is an algebraically closed field.
        # We evaluate this over the complex numbers (implicitly), so we just need to verify 
        # that the witness is a valid polynomial in x and y.
        h1 = (isinstance(witness, sympy.Expr) and 
              witness.free_symbols.issubset({x, y}) and 
              witness.is_polynomial(x, y))
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # ¬Q: The equation f(x, y) = 0 has finitely many distinct solutions in K x K.
            # Over an algebraically closed field, a polynomial equation f(x, y) = 0 has finitely 
            # many solutions if and only if f is a non-zero constant (in which case it has 0 solutions).
            # If f is the zero polynomial, it has infinitely many solutions.
            # If f is non-constant, it has infinitely many solutions.
            p = sympy.Poly(witness, x, y)
            # A non-zero constant polynomial has a total degree of exactly 0.
            # (The zero polynomial has a degree of -oo).
            neg_q = (p.degree() == 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: The equation f(x, y) = 0 has finitely many distinct solutions in K x K"
]

N_HYP = 1
NEG_Q_INDEX = 1