import sympy
from sympy import Symbol, Poly, sqrt, I, QQ
from sympy.abc import x

# Setup
x = Symbol('x')
f = (x**3 - 1)*(x**2 - 11)
sqrt_minus_3 = sqrt(-3)
sqrt_11 = sqrt(11)
try:
    K_expected = QQ.algebraic_field(sqrt_minus_3, sqrt_11)
except Exception:
    K_expected = None

def conditions(witness):
    try:
        # H1: f(x) = (x^3-1)(x^2-11) \in Q[x]
        h1 = all(c.is_rational for c in Poly(f, x).coeffs())
    except Exception:
        h1 = False
        
    try:
        concl = False
        if K_expected is not None and witness == K_expected:
            concl = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            if K_expected is not None and witness[0] == K_expected and witness[1] == 4:
                concl = True
            elif isinstance(witness[0], (set, list, tuple)):
                gens = set(witness[0])
                if gens == {sqrt_minus_3, sqrt_11} and witness[1] == 4:
                    concl = True
        elif isinstance(witness, (set, list, tuple)):
            gens = set(witness)
            if gens == {sqrt_minus_3, sqrt_11}:
                concl = True
        elif isinstance(witness, dict):
            if K_expected is not None and witness.get('K') == K_expected and witness.get('degree') == 4:
                concl = True
            elif isinstance(witness.get('K'), (set, list, tuple)):
                gens = set(witness['K'])
                if gens == {sqrt_minus_3, sqrt_11} and witness.get('degree') == 4:
                    concl = True
    except Exception:
        concl = False
        
    neg_q = not concl
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = (x^3-1)(x^2-11) in Q polynomials",
    "¬Q: K != Q(sqrt(-3), sqrt(11)) or degree of K over Q != 4"
]

N_HYP = 1
NEG_Q_INDEX = 1