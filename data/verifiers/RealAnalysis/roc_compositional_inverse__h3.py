import sympy
from sympy.abc import x

# Top-level setup
# (No specific named groups or matrices are required for this real analysis conjecture)

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the conjecture.
    The witness can be a sympy expression in `x`, a list/tuple of coefficients, 
    or a callable function.
    """
    try:
        if isinstance(witness, (list, tuple)):
            f = sum(c * x**i for i, c in enumerate(witness))
        elif callable(witness):
            f = witness(x)
        else:
            f = witness
            
        f = sympy.sympify(f)
    except Exception:
        return [False, False, False]
        
    # H_1: f(x) is a power series with a strictly positive radius of convergence.
    # We verify this by checking if it is analytic at 0 (its Taylor series up to degree 5 is a polynomial).
    try:
        s = f.series(x, 0, 5).removeO()
        h1_ok = bool(s.is_polynomial(x))
    except Exception:
        h1_ok = False
        
    # H_2: Assume the constant term a_0 = 0.
    try:
        a0 = f.subs(x, 0)
        h2_ok = bool(sympy.simplify(a0) == 0)
    except Exception:
        h2_ok = False
        
    # ¬Q: The formal compositional inverse series does NOT have a strictly positive radius of convergence.
    # By the Inverse Function Theorem, if f is analytic at 0 and f'(0) != 0, the inverse is analytic 
    # (has a strictly positive radius of convergence). If f'(0) == 0, the formal compositional inverse 
    # series does not even exist, so it trivially fails to have a strictly positive radius of convergence.
    try:
        a1 = f.diff(x).subs(x, 0)
        neg_q_ok = bool(sympy.simplify(a1) == 0)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is a power series with a strictly positive radius of convergence",
    "H_2: The constant term a_0 is 0",
    "¬Q: The formal compositional inverse series does not exist or has zero radius of convergence"
]

N_HYP = 2
NEG_Q_INDEX = 2