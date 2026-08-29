import sympy
from sympy import Symbol, diff, S, oo
from sympy.calculus.util import continuous_domain, function_range

# Define the variable that might be used in the witness expression
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "The function f is not uniformly continuous on R."
    
    A counterexample must be a function that IS uniformly continuous on R.
    """
    try:
        # Handle both callable functions and SymPy expressions
        if callable(witness):
            expr = witness(x)
        else:
            expr = witness
        expr = sympy.sympify(expr)
    except Exception:
        return [False]
        
    neg_q = False
    try:
        # A sufficient condition for uniform continuity on R is that the function
        # is continuous on R and its derivative is bounded on R.
        dom = continuous_domain(expr, x, S.Reals)
        if dom == S.Reals:
            df = diff(expr, x)
            if df.is_constant():
                neg_q = True
            else:
                rng = function_range(df, x, S.Reals)
                if rng.sup < oo and rng.inf > -oo:
                    neg_q = True
    except Exception:
        pass
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: f is uniformly continuous on R"
]

N_HYP = 0
NEG_Q_INDEX = 0