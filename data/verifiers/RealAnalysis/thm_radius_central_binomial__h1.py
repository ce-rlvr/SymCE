import sympy
from sympy import Symbol, limit, Limit, oo, Abs, Rational, simplify

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, nonnegative=True)
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any sequence a_n, the radius of convergence 
    of sum(a_n x^n) is 1/4.
    """
    try:
        # Evaluate the witness to get the expression for a_n
        if callable(witness):
            a_n = sympy.sympify(witness(n))
        else:
            a_n = sympy.sympify(witness)
            
        # Attempt to compute the radius of convergence using the ratio test
        a_n_plus_1 = a_n.subs(n, n + 1)
        ratio = Abs(a_n / a_n_plus_1)
        R = limit(ratio, n, oo)
        
        # If the ratio test limit is unevaluated or undefined, fallback to the root test
        if R.has(limit) or R.has(Limit) or R.has(sympy.nan):
            root = Abs(a_n)**(1/n)
            L = limit(root, n, oo)
            if L == 0:
                R = oo
            elif L == oo:
                R = sympy.Integer(0)
            elif not (L.has(limit) or L.has(Limit) or L.has(sympy.nan)):
                R = 1 / L

        # Check if the radius of convergence is exactly 1/4
        if R == Rational(1, 4):
            neg_q = False
        elif R.has(limit) or R.has(Limit) or R.has(sympy.nan):
            # If we still cannot evaluate the limit, we cannot confirm it fails
            neg_q = False
        else:
            # Check if the difference simplifies to 0
            diff = simplify(R - Rational(1, 4))
            if diff == 0:
                neg_q = False
            else:
                neg_q = True
                
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series sum(a_n x^n) is not equal to 1/4"
]

N_HYP = 0
NEG_Q_INDEX = 0