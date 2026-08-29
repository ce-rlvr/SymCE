import sympy
from sympy import sqrt, Rational, Poly
from sympy.polys.domains import QQ
from sympy.abc import x

# Top-level setup
sqrt_minus_3 = sqrt(-3)
cbrt_2 = 2**(Rational(1, 3))

F_expected = QQ.algebraic_field(sqrt_minus_3)
f_expected = Poly(x**3 - 2, x, domain=F_expected)
K_expected = QQ.algebraic_field(sqrt_minus_3, cbrt_2)

CONDITION_LABELS = [
    "H_1: F is Q(sqrt(-3))",
    "H_2: f(x) is x^3 - 2 over F",
    "¬Q: K is not F(cbrt(2)) or degree over F is not 3"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            F_wit = witness.get('F', F_expected)
            f_wit = witness.get('f', f_expected)
            K_wit = witness.get('K', witness)
        elif isinstance(witness, tuple) and len(witness) == 3:
            F_wit, f_wit, K_wit = witness
        else:
            F_wit = F_expected
            f_wit = f_expected
            K_wit = witness
            
        h1 = (F_wit == F_expected)
        
        if isinstance(f_wit, Poly):
            h2 = (f_wit == f_expected)
        else:
            h2 = (f_wit == x**3 - 2)
            
        q = False
        if isinstance(K_wit, tuple) and len(K_wit) == 2:
            K_obj, deg = K_wit
            q = (K_obj == K_expected) and (deg == 3)
        elif isinstance(K_wit, dict):
            K_obj = K_wit.get('K', K_wit)
            deg = K_wit.get('degree', 3)
            q = (K_obj == K_expected) and (deg == 3)
        else:
            if K_wit == K_expected:
                q = True
            else:
                q = False
                
        neg_q = not q
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]