import sympy
from sympy import S, Interval, Union, Intersection, FiniteSet, ProductSet, ImageSet, Lambda, Symbol, oo, pi, E

# Top-level setup for potential witness expressions
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
n = Symbol('n', integer=True)

def conditions(witness):
    try:
        # The witness K is expected to be a SymPy Set representing a subset of R^n.
        bnd = witness.boundary
        
        # In R^n, a set is compact if and only if it is closed and bounded.
        # The boundary of any set is always closed.
        # Therefore, the boundary is compact iff it is bounded.
        is_bnd = bnd.is_bounded
        is_cl = bnd.is_closed
        
        if is_bnd is False or is_cl is False:
            neg_q = True
        elif is_bnd is True and is_cl is True:
            neg_q = False
        else:
            # Fallback if properties are not explicitly evaluated by SymPy
            bounded = is_bnd
            if bounded is None:
                try:
                    if bnd.inf == -oo or bnd.sup == oo:
                        bounded = False
                    elif bnd.inf.is_real and bnd.sup.is_real:
                        bounded = True
                except Exception:
                    if isinstance(bnd, ProductSet):
                        if any(c.is_bounded is False for c in bnd.args):
                            bounded = False
                        elif all(c.is_bounded is True for c in bnd.args):
                            bounded = True
            
            if bounded is False:
                neg_q = True
            elif bounded is True:
                neg_q = False
            else:
                neg_q = False
                
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The boundary of K is not a compact subset of R^n"
]

N_HYP = 0
NEG_Q_INDEX = 0