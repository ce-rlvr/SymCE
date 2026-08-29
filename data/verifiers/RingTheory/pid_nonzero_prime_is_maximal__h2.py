import sympy
from sympy import ZZ, QQ, Symbol

x = Symbol('x')
QQ_x = QQ[x]
ZZ_x = ZZ[x]

def conditions(witness):
    """
    Given a witness, which can be a tuple (R, p) representing the domain R and 
    the generator p of the ideal P, or just p (defaulting to R = ZZ),
    returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, p = witness
        else:
            R = ZZ
            p = witness
            
        # Extract generator if an ideal object was passed
        if hasattr(p, 'gen'):
            p = p.gen
        elif hasattr(p, 'gens') and len(p.gens) == 1:
            p = p.gens[0]
    except Exception:
        return [False, False]
        
    # H_1: R is a Principal Ideal Domain (PID)
    try:
        if R == ZZ or R == QQ_x:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # neg_Q: P is not a maximal ideal of R
    try:
        is_maximal = False
        if R == ZZ:
            try:
                val = abs(int(p))
                is_maximal = sympy.isprime(val)
            except Exception:
                is_maximal = False
        elif R == QQ_x:
            try:
                if p == 0:
                    is_maximal = False
                else:
                    poly = sympy.Poly(p, x)
                    if poly.degree() <= 0:
                        is_maximal = False
                    else:
                        coeff, factors = sympy.factor_list(p, domain='QQ')
                        if len(factors) == 1 and factors[0][1] == 1:
                            is_maximal = True
                        else:
                            is_maximal = False
            except Exception:
                is_maximal = False
        else:
            # Fallback for generic domains
            try:
                if p == 0:
                    is_maximal = False
                else:
                    val = abs(int(p))
                    is_maximal = sympy.isprime(val)
            except Exception:
                is_maximal = False
                        
        neg_q = not is_maximal
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Principal Ideal Domain (PID)",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1