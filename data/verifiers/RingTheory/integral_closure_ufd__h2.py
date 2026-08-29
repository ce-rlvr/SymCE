import sympy
from sympy import Poly, Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a UFD with field of fractions K, and \alpha \in K is a root of f, 
    then \alpha \in R."
    (The dropped hypothesis is that f must be a monic polynomial).
    
    We restrict our check to the standard UFD R = ZZ, with K = QQ.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Parse witness
        if isinstance(witness, dict):
            f = witness.get('f')
            alpha = witness.get('alpha')
        elif isinstance(witness, tuple) and len(witness) == 2:
            f, alpha = witness
        elif isinstance(witness, tuple) and len(witness) == 3:
            _, f, alpha = witness
        else:
            return [False, False, False]
            
        if f is None or alpha is None:
            return [False, False, False]
            
        f = sympy.sympify(f)
        
        # Determine the variable of the polynomial
        free_symbols = getattr(f, 'free_symbols', set())
        if len(free_symbols) >= 1:
            var = sorted(list(free_symbols), key=lambda s: s.name)[0]
        else:
            var = x
            
        # H_1: R is a Unique Factorization Domain with field of fractions K
        # We interpret this as f being a polynomial over R = ZZ.
        try:
            poly_f = Poly(f, var, domain='ZZ')
            h1 = True
        except Exception:
            h1 = False
            
        # H_2: \alpha \in K is a root of f
        # K is QQ, so alpha must be a rational number, and f(alpha) == 0.
        try:
            alpha_rat = Rational(alpha)
            val = f.subs(var, alpha_rat)
            h2 = (sympy.simplify(val) == 0)
        except Exception:
            h2 = False
            
        # ¬Q: \alpha is not an element of R
        # R is ZZ, so alpha must not be an integer.
        try:
            alpha_rat = Rational(alpha)
            neg_q = (alpha_rat.q != 1)
        except Exception:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: R is a Unique Factorization Domain with field of fractions K",
    r"H_2: \alpha \in K is a root of f",
    r"¬Q: \alpha is not an element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2