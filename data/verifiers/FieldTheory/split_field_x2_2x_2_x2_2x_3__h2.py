import sympy
from sympy import Symbol, expand, QQ, I, sqrt

x = Symbol('x')

def conditions(witness):
    expected_f = (x**2 - 2*x + 2)*(x**2 - 2*x + 3)
    
    if isinstance(witness, tuple) and len(witness) == 2:
        if hasattr(witness[0], 'free_symbols') and x in witness[0].free_symbols:
            f, K_obj = witness
        else:
            f = expected_f
            K_obj = witness
    else:
        f = expected_f
        K_obj = witness

    try:
        h1_ok = (expand(f - expected_f) == 0)
    except Exception:
        h1_ok = False

    try:
        expected_K1 = QQ.algebraic_field(I, sqrt(2))
        expected_K2 = QQ.algebraic_field(sqrt(2), I)
        
        if isinstance(K_obj, (list, tuple, set)):
            K_field = QQ.algebraic_field(*K_obj)
        else:
            K_field = K_obj
            
        if K_field == expected_K1 or K_field == expected_K2:
            q_ok = True
        else:
            try:
                deg = K_field.ext.minpoly.degree()
            except AttributeError:
                try:
                    deg = K_field.ext.minpoly.as_poly().degree()
                except AttributeError:
                    deg = None
                    
            if deg == 4:
                try:
                    K_field.from_sympy(I)
                    K_field.from_sympy(sqrt(2))
                    q_ok = True
                except Exception:
                    try:
                        K_field(I)
                        K_field(sqrt(2))
                        q_ok = True
                    except Exception:
                        q_ok = False
            else:
                q_ok = False
                
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = True

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f(x) = (x^2-2x+2)(x^2-2x+3) in Q polynomials",
    "neg_Q: K != Q(i, sqrt(2)) or degree != 4"
]

N_HYP = 1
NEG_Q_INDEX = 1