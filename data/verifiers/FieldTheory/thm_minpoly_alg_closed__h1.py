import sympy
from sympy import Symbol, QQ, ZZ, RR, CC, I, sqrt, Rational, minpoly, simplify, expand

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (F, K, alpha)
    where F and K are SymPy domains (e.g., QQ, QQ.algebraic_field(sqrt(2)))
    and alpha is a SymPy expression (e.g., sqrt(2)).
    """
    try:
        F, K, alpha = witness
    except Exception:
        return [False, False, False]
        
    # H_1: K is an extension field of F
    try:
        is_F_field = getattr(F, 'is_Field', False)
        is_K_field = getattr(K, 'is_Field', False)
        
        # Check if F is a subfield of K
        is_extension = (
            (F == K) or 
            (hasattr(K, 'domain') and K.domain == F) or 
            (F == QQ) or 
            (F == RR and K == CC)
        )
        
        h1_ok = bool(is_F_field and is_K_field and is_extension)
    except Exception:
        h1_ok = False
        
    # H_2: \alpha \in K is algebraic over F
    try:
        # Check if alpha belongs to K
        K.from_sympy(alpha)
        
        # Check if alpha is algebraic over F
        mp = minpoly(alpha, x, domain=F)
        h2_ok = bool(mp is not None and mp.has(x))
    except Exception:
        h2_ok = False
        
    # ¬Q: The minimal polynomial of \alpha over F is not x - \alpha
    try:
        mp = minpoly(alpha, x, domain=F)
        expected = x - alpha
        # If the minimal polynomial is not x - alpha, the conclusion fails (neg_Q is True)
        neg_q_ok = bool(simplify(expand(mp - expected)) != 0)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an extension field of F",
    "H_2: alpha in K is algebraic over F",
    "¬Q: The minimal polynomial of alpha over F is not x - alpha"
]

N_HYP = 2
NEG_Q_INDEX = 2