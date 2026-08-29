import sympy

# Top-level setup
x = sympy.Symbol('x', real=True)

class DirichletFunction:
    """Dirichlet function: 1 on rationals, 0 on irrationals. Nowhere continuous, nowhere differentiable."""
    pass

class WeierstrassFunction:
    """Weierstrass function: continuous everywhere, differentiable nowhere."""
    pass

class BrownianMotionPath:
    """A sample path of Brownian motion: continuous everywhere, differentiable nowhere with probability 1."""
    pass

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (U, f) where U is the domain and f is the function.
    """
    try:
        U, f = witness
    except Exception:
        return [False, False]
    
    # H_1: U is an open subset of R
    try:
        h1 = False
        if hasattr(U, 'is_subset') and hasattr(U, 'is_open'):
            if (U.is_subset(sympy.S.Reals) == True) and (U.is_open == True):
                h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: f is not differentiable almost everywhere on U
    try:
        neg_q = False
        
        # If U is empty or has measure 0, any function is vacuously differentiable a.e. on U
        if hasattr(U, 'is_empty') and U.is_empty == True:
            pass
        elif hasattr(U, 'measure') and U.measure == 0:
            pass
        else:
            if isinstance(f, (DirichletFunction, WeierstrassFunction, BrownianMotionPath)):
                neg_q = True
            elif hasattr(f, 'is_differentiable_ae'):
                neg_q = not f.is_differentiable_ae
            elif callable(f):
                # Heuristic check for Dirichlet-like or Thomae-like functions
                rats = [sympy.Rational(1, 2), sympy.Rational(1, 3), sympy.Rational(4, 5), sympy.Rational(5, 2), sympy.Rational(-1, 2)]
                irrats = [sympy.pi, sympy.sqrt(2), sympy.exp(1), sympy.sqrt(3), -sympy.pi]
                
                v_rats = [f(r) for r in rats]
                v_irrats = [f(i) for i in irrats]
                
                if len(set(v_rats)) == 1 and len(set(v_irrats)) == 1 and v_rats[0] != v_irrats[0]:
                    neg_q = True
                elif len(set(v_irrats)) == 1 and v_irrats[0] == 0:
                    if all(v != 0 for v in v_rats):
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open subset of R",
    "¬Q: f is not differentiable almost everywhere on U"
]

N_HYP = 1
NEG_Q_INDEX = 1