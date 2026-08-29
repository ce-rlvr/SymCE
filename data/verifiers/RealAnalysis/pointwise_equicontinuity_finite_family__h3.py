import sympy
from sympy import Symbol, Piecewise, S, Heaviside, sign
from sympy.calculus.util import continuous_domain

# Top-level setup: named object bindings that the witness expression may reference.
# We define a real symbol 'x' and common discontinuous functions to help construct a witness.
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "A finite family of functions from metric space X to Y is equicontinuous at every point."
    
    The true theorem requires the functions to be continuous.
    """
    # H_1: X and Y are metric spaces.
    # We evaluate the witness over X = Y = R with the standard metric, which are valid metric spaces.
    h1_ok = True
    
    # H_2: F is a finite set of functions from X to Y.
    h2_ok = False
    funcs = []
    try:
        if isinstance(witness, sympy.Expr):
            funcs = [witness]
            h2_ok = True
        elif isinstance(witness, (list, tuple, set)):
            funcs = list(witness)
            h2_ok = all(isinstance(f, sympy.Expr) for f in funcs)
    except Exception:
        h2_ok = False
        funcs = []
        
    # ¬Q: The family F is NOT equicontinuous at every point x in X.
    # Since F is finite, equicontinuity at every point is equivalent to every function in F
    # being continuous at every point. Thus, the conclusion fails (¬Q is True) if there is 
    # at least one function in F that is discontinuous somewhere in R.
    neg_q_ok = False
    try:
        for f in funcs:
            free_syms = f.free_symbols
            if not free_syms:
                # Constant functions are continuous everywhere
                continue
            
            is_continuous_everywhere = True
            for sym in free_syms:
                # Find the domain of continuity for the function over the Reals
                dom = continuous_domain(f, sym, sympy.S.Reals)
                if dom != sympy.S.Reals:
                    is_continuous_everywhere = False
                    break
            
            if not is_continuous_everywhere:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X and Y are metric spaces",
    "H_2: F is a finite set of functions from X to Y",
    "¬Q: F is not equicontinuous at every point x in X"
]

N_HYP = 2
NEG_Q_INDEX = 2