import sympy
from sympy import Symbol, S, diff, Set
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup: named object bindings that the witness expression may reference.
# The witness is expected to be a tuple: (domain, f, g)
# where domain is a SymPy Set (e.g., S.Reals), and f, g are SymPy expressions in x.
x = Symbol('x', real=True)

def is_lipschitz(expr, domain):
    """
    Checks if a SymPy expression is Lipschitz continuous on the given domain
    by verifying that its derivative is bounded.
    """
    try:
        expr = sympy.sympify(expr)
        
        # Check if the function is continuous on the domain
        cd = continuous_domain(expr, x, S.Reals)
        if not domain.is_subset(cd):
            return False
            
        # Check if the derivative is bounded on the domain
        deriv = diff(expr, x)
        fr = function_range(deriv, x, domain)
        
        if hasattr(fr, 'inf') and hasattr(fr, 'sup'):
            return fr.inf.is_finite and fr.sup.is_finite
            
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        domain, f, g = witness
    except Exception:
        return [False, False, False]
        
    # H_1: X is a metric space (represented here as a non-empty SymPy Set)
    try:
        h1 = isinstance(domain, Set) and not domain.is_empty
    except Exception:
        h1 = False
        
    # H_2: f and g are Lipschitz continuous on X
    try:
        h2 = is_lipschitz(f, domain) and is_lipschitz(g, domain)
    except Exception:
        h2 = False
        
    # ¬Q: The product function fg is NOT Lipschitz continuous on X
    try:
        fg = f * g
        neg_q = not is_lipschitz(fg, domain)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: f and g are Lipschitz continuous on X",
    "¬Q: fg is not Lipschitz continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2