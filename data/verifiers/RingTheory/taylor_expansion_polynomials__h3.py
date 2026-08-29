import sympy
from sympy import Symbol, Poly, S
from sympy.polys.domains import Domain
from sympy import ZZ, QQ, RR, CC

x = Symbol('x')

def is_comm_ring(R):
    try:
        if isinstance(R, Domain):
            return True
        if R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            return True
        if hasattr(R, 'is_commutative') and R.is_commutative and hasattr(R, 'is_ring') and R.is_ring:
            return True
        return False
    except Exception:
        return False

def in_R(c, R):
    from sympy import sympify
    try:
        c = sympify(c)
        if hasattr(R, 'contains'):
            res = R.contains(c)
            if res in (True, False):
                return bool(res)
        if hasattr(R, '__contains__'):
            return c in R
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        R, a, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring
    try:
        h1 = is_comm_ring(R)
    except Exception:
        h1 = False
        
    # H_2: a is an element of R
    try:
        h2 = in_R(a, R)
    except Exception:
        h2 = False
        
    # ¬Q: f(x) cannot be uniquely expressed as a polynomial in (x-a) over R
    try:
        f = sympy.sympify(f)
        y = Symbol('y')
        f_y = f.subs(x, y + a)
        p = Poly(f_y, y)
        
        all_in_R = True
        for c in p.all_coeffs():
            if not in_R(c, R):
                all_in_R = False
                break
                
        neg_q = not all_in_R
    except Exception:
        # If Poly fails, f(x) is not a polynomial, so it cannot be expressed as such
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: a is an element of R",
    "¬Q: f(x) cannot be uniquely expressed as a polynomial in (x-a) over R"
]

N_HYP = 2
NEG_Q_INDEX = 2