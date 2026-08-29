import sympy
from sympy.ntheory import totient

CONDITION_LABELS = [
    "H_1: \phi is Euler's totient function",
    "H_2: x is a complex number such that |x| < 1/p",
    "¬Q: \sum_{k=0}^{\infty} \phi(p^k) x^k != (1-x)/(1-px)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H1: \phi is Euler's totient function
    h1 = True
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            p, x = witness
        else:
            p = int(witness)
            x = 1.0 / (2 * p) if p != 0 else 0
    except Exception:
        p, x = None, None

    # H2: x is a complex number such that |x| < 1/p
    h2 = False
    if p is not None and x is not None:
        try:
            p_int = int(p)
            if p_int >= 1 and p_int == p:
                h2 = abs(complex(x)) < 1.0 / p_int
        except Exception:
            h2 = False

    # neg_Q: conclusion fails
    neg_q = False
    if p is not None and x is not None:
        try:
            p_int = int(p)
            phi_p = totient(p_int)
            
            denom = 1 - p_int * x
            is_zero = False
            try:
                is_zero = abs(complex(denom)) < 1e-12
            except TypeError:
                is_zero = sympy.simplify(denom) == 0
                
            if is_zero:
                neg_q = True
            else:
                lhs = 1 + phi_p * x / (1 - p_int * x)
                rhs = (1 - x) / (1 - p_int * x)
                
                try:
                    neg_q = abs(complex(lhs) - complex(rhs)) > 1e-9
                except TypeError:
                    diff = sympy.simplify(lhs - rhs)
                    neg_q = diff != 0
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]