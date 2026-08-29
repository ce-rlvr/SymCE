from sympy import Symbol, sympify, isprime, Poly
from sympy.polys.domains import ZZ, QQ

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: P is a prime ideal of R",
    "¬Q: There does not exist a prime ideal Q of S such that Q ∩ R = P"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        R, S, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R and S are commutative rings with identity
    try:
        h1 = hasattr(R, 'unify') and hasattr(S, 'unify') and hasattr(R, 'from_sympy') and hasattr(S, 'from_sympy')
    except Exception:
        h1 = False
        
    # H_2: R is a subring of S
    try:
        h2 = (R.unify(S) == S)
    except Exception:
        h2 = False
        
    # H_3: P is a prime ideal of R
    try:
        h3 = False
        if R == ZZ:
            if P == 0:
                h3 = True
            else:
                h3 = isprime(abs(int(P)))
        elif R == QQ or getattr(R, 'is_Field', False):
            h3 = (P == 0)
        else:
            if P == 0:
                h3 = True
            else:
                h3 = Poly(P).is_irreducible
    except Exception:
        h3 = False
        
    # ¬Q: There does not exist a prime ideal Q of S such that Q ∩ R = P
    try:
        neg_q = False
        if S == QQ or getattr(S, 'is_Field', False):
            neg_q = (P != 0)
        else:
            try:
                p_sym = sympify(P)
                p_s = S.from_sympy(p_sym)
                if p_s is not None:
                    S.exquo(S.one, p_s)
                    neg_q = True
            except Exception:
                pass
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]