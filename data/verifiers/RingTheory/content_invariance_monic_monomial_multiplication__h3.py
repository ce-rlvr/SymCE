import sympy as sp
from sympy import Poly, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial",
    "not Q: The content of x^k f is not associate to the content of f"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    x = Symbol('x')
    
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, k = witness
            elif len(witness) == 3:
                _, f, k = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: R is a UFD
    try:
        f_expr = sp.sympify(f)
        poly_f = Poly(f_expr, x)
        domain = poly_f.domain
        h1 = bool(domain.is_UFD)
    except Exception:
        h1 = False
        
    # H2: f is a non-zero polynomial
    try:
        f_expr = sp.sympify(f)
        poly_f = Poly(f_expr, x)
        h2 = not poly_f.is_zero
    except Exception:
        h2 = False
        
    # neg_Q: The content of x^k f is NOT associate to the content of f
    try:
        f_expr = sp.sympify(f)
        poly_f = Poly(f_expr, x)
        c_f = poly_f.content()
        
        g = sp.expand(x**k * f_expr)
        
        try:
            poly_g = Poly(g, x)
            c_g = poly_g.content()
            
            if c_f == c_g or c_f == -c_g:
                q_holds = True
            elif poly_f.domain.is_Field and c_f != 0 and c_g != 0:
                q_holds = True
            else:
                domain = poly_f.domain
                try:
                    q1, r1 = domain.div(c_f, c_g)
                    q2, r2 = domain.div(c_g, c_f)
                    q_holds = (r1 == 0 and r2 == 0)
                except Exception:
                    q_holds = False
        except Exception:
            # If g is not a polynomial, it doesn't have a content
            q_holds = False
            
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]