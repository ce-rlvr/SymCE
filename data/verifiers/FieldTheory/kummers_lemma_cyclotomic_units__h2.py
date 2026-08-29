import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: u is a unit in the ring of integers Z(zeta_p)",
    "¬Q: u is not of the form zeta_p^k v for any v in the real subring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        p, U = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = sp.isprime(p) and p % 2 == 1
    except Exception:
        h1 = False

    try:
        x = sp.Symbol('x')
        if isinstance(U, (list, tuple)):
            U_poly = sum(c * x**i for i, c in enumerate(U))
        else:
            U_expr = sp.sympify(U)
            free_syms = U_expr.free_symbols
            if free_syms:
                sym = list(free_syms)[0]
                U_poly = U_expr.subs(sym, x)
            else:
                U_poly = U_expr
        
        U_poly = sp.expand(U_poly)
        
        if isinstance(p, int) and p > 0:
            Phi = sp.cyclotomic_poly(p, x)
            poly_obj = sp.Poly(U_poly, x)
            if not all(c.is_integer for c in poly_obj.coeffs()):
                h2 = False
            else:
                norm = sp.resultant(U_poly, Phi, x)
                h2 = (abs(norm) == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = True
        if isinstance(p, int) and p > 0:
            Phi = sp.cyclotomic_poly(p, x)
            U_bar = sp.rem(sp.expand(U_poly.subs(x, x**(p-1))), Phi, x)
            U_bar = sp.expand(U_bar)
            
            for m in range(p):
                lhs = sp.rem(sp.expand(U_poly * x**m), Phi, x)
                lhs = sp.expand(lhs)
                if sp.expand(lhs - U_bar) == 0:
                    neg_q = False
                    break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]