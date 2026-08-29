import sympy as sp
from sympy.abc import x, y, z

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is a polynomial",
    "¬Q: f nilpotent iff c(f) in nilradical"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_zero_elem(p):
    if p == 0:
        return True
    if hasattr(p, 'is_zero') and p.is_zero:
        return True
    if isinstance(p, sp.Poly) and p.is_zero:
        return True
    if isinstance(p, sp.MatrixBase) and p.is_zero_matrix:
        return True
    return False

def check_nilpotent(elem, max_deg=30):
    if is_zero_elem(elem):
        return True
    p = elem
    for _ in range(1, max_deg):
        try:
            p = p * elem
            if hasattr(p, 'expand'):
                p = sp.expand(p)
        except Exception:
            pass
        if is_zero_elem(p):
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, f = witness
            else:
                return [False, False, False]
        else:
            f = witness
            R = getattr(f, 'domain', None)
    except Exception:
        return [False, False, False]

    try:
        h1 = True
        if R is not None:
            if hasattr(R, 'is_commutative') and R.is_commutative is False:
                h1 = False
            if hasattr(R, 'has_Identity') and R.has_Identity is False:
                h1 = False
        
        if isinstance(f, sp.Poly):
            coeffs = f.coeffs()
        elif hasattr(f, 'coeffs') and callable(f.coeffs):
            coeffs = f.coeffs()
        else:
            coeffs = sp.Poly(f).coeffs()
            
        for c in coeffs:
            if getattr(c, 'is_commutative', None) is False:
                h1 = False
            if isinstance(c, sp.MatrixBase):
                h1 = False
    except Exception:
        h1 = False

    try:
        h2 = False
        if isinstance(f, sp.Poly):
            h2 = True
        elif hasattr(f, 'is_polynomial'):
            if callable(f.is_polynomial):
                try:
                    h2 = bool(f.is_polynomial())
                except Exception:
                    h2 = False
            else:
                h2 = bool(f.is_polynomial)
        else:
            try:
                sp.Poly(f)
                h2 = True
            except Exception:
                pass
    except Exception:
        h2 = False

    try:
        f_is_nil = check_nilpotent(f)
        
        if isinstance(f, sp.Poly):
            coeffs = f.coeffs()
        elif hasattr(f, 'coeffs') and callable(f.coeffs):
            coeffs = f.coeffs()
        else:
            coeffs = sp.Poly(f).coeffs()
            
        coeffs_nil = True
        for c in coeffs:
            if not check_nilpotent(c):
                coeffs_nil = False
                break
                
        q = (f_is_nil == coeffs_nil)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]