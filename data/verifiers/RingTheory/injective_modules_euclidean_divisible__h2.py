import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x

# Top-level setup for witness expressions
QQ_x = QQ[x]
ZZ_x = ZZ[x]
QQ_frac_x = QQ.frac_field(x)

def is_euclidean_domain(R):
    """Check if R is a Euclidean domain."""
    if R in (ZZ, QQ, RR, CC):
        return True
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if hasattr(R, 'is_PID') and R.is_PID:
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        # Polynomial ring over a field in 1 variable is a Euclidean domain
        if R.domain.is_Field and len(R.symbols) == 1:
            return True
    return False

def is_divisible(R, M):
    """Check if M is a divisible R-module."""
    if R == ZZ and M == ZZ:
        return False
    if R == ZZ and M == QQ:
        return True
    if R == QQ_x and M == QQ_x:
        return False
    if R == QQ_x and M == QQ_frac_x:
        return True
    
    r_test = []
    if R == ZZ:
        r_test = [2, 3]
    elif hasattr(R, 'gens') and len(R.gens) > 0:
        r_test = [R.gens[0]]
    
    m_test = []
    if M == ZZ:
        m_test = [1]
    elif M == QQ:
        m_test = [1]
    elif hasattr(M, 'gens') and len(M.gens) > 0:
        m_test = [M.gens[0]]
    elif hasattr(M, 'one'):
        m_test = [M.one]
        
    if not r_test or not m_test:
        if M == R and R not in (QQ, RR, CC) and not (hasattr(R, 'is_Field') and R.is_Field):
            return False
        return True
        
    for r in r_test:
        for m in m_test:
            try:
                if M == ZZ:
                    if sympy.Rational(m, r).q != 1:
                        return False
                elif hasattr(M, 'exquo'):
                    try:
                        M.exquo(m, r)
                    except Exception:
                        return False
                else:
                    res = m / r
                    if hasattr(M, 'from_sympy'):
                        try:
                            M.from_sympy(res)
                        except Exception:
                            return False
                    elif res not in M:
                        return False
            except Exception:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        R, M = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_euclidean_domain(R)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_divisible(R, M)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: M is not a divisible module"
]

N_HYP = 1
NEG_Q_INDEX = 1