import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x')
n = sp.Symbol('n', integer=True)
alpha_sym = sp.Symbol('alpha', real=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be the value of alpha), evaluates the hypotheses
    and the negated conclusion.
    """
    h1 = False
    alpha_val = None
    
    try:
        # Extract alpha from dictionary if provided, otherwise assume witness is alpha
        if isinstance(witness, dict) and 'alpha' in witness:
            val = witness['alpha']
        else:
            val = witness
            
        # Check if alpha is a real number and extract its float value
        if isinstance(val, (int, float)):
            alpha_val = float(val)
            h1 = True
        elif isinstance(val, complex):
            if val.imag == 0:
                alpha_val = float(val.real)
                h1 = True
        elif isinstance(val, str):
            try:
                alpha_val = float(val)
                h1 = True
            except ValueError:
                pass
        elif hasattr(val, 'is_real') and val.is_real:
            alpha_val = float(val.evalf())
            h1 = True
        elif isinstance(val, sp.Expr):
            eval_val = val.evalf()
            if eval_val.is_real:
                alpha_val = float(eval_val)
                h1 = True
    except Exception:
        pass

    # H2: The power series is defined as sum_{n=0}^infty (-1)^n / (n! Gamma(n+alpha+1)) x^n
    # This is a descriptive hypothesis establishing the context for the series.
    h2 = True

    neg_q = False
    try:
        if h1 and alpha_val is not None:
            # The conclusion is that the radius of convergence is infinity.
            # This fails (neg_Q is True) if the series is undefined.
            # The series is undefined when Gamma(n+alpha+1) has poles for some n >= 0,
            # which occurs exactly when alpha is a negative integer.
            if alpha_val < 0 and alpha_val.is_integer():
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is a real number",
    "H_2: The power series is defined as sum_{n=0}^infty (-1)^n / (n! Gamma(n+alpha+1)) x^n",
    "¬Q: The radius of convergence of the power series is not infinity"
]

N_HYP = 2
NEG_Q_INDEX = 2