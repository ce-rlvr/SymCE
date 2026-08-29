import sympy as sp
from sympy.abc import x, y, z, t, alpha, beta

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let E/F be a field extension. The element alpha is separable over F if and only if 
    the simple extension F(alpha) is a separable extension of F."
    
    The dropped hypothesis is that alpha must be algebraic over F. 
    If alpha is transcendental, it is not a separable element (as it is not algebraic), 
    but the purely transcendental extension F(alpha)/F is a separable extension 
    (it has a separating transcendence basis). Thus the biconditional fails.
    """
    try:
        # H_1: E/F is a field extension
        # We accept a string 'transcendental' or a SymPy Symbol as a transcendental element.
        # We accept a SymPy Poly as an algebraic element (representing its minimal polynomial).
        if witness == 'transcendental' or isinstance(witness, sp.Symbol):
            h1 = True
            # A transcendental element is not algebraic, hence not a separable element.
            alpha_is_separable = False
            # However, a purely transcendental extension F(alpha)/F is a separable extension.
            F_alpha_is_separable_ext = True
            
        elif isinstance(witness, sp.Poly):
            h1 = True
            # For an algebraic element, it is separable iff its minimal polynomial has a non-zero formal derivative.
            alpha_is_separable = not witness.diff().is_zero
            # For algebraic extensions, F(alpha) is a separable extension iff alpha is a separable element.
            F_alpha_is_separable_ext = alpha_is_separable
            
        else:
            h1 = False
            alpha_is_separable = False
            F_alpha_is_separable_ext = False

        # The conclusion is the biconditional between the two properties
        iff_holds = (alpha_is_separable == F_alpha_is_separable_ext)
        
        # neg_Q is True when the conclusion FAILS
        neg_q = not iff_holds

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "¬Q: The equivalence between alpha being a separable element and F(alpha) being a separable extension FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1