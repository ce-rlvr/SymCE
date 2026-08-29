import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x

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

def conditions(witness):
    try:
        f_expr = sp.sympify(witness)
        f_poly = sp.Poly(f_expr, x, domain='QQ')
        
        h1 = bool(f_poly.is_irreducible)
        h2 = h1
        
        if not h1:
            return [False, False, False]
            
        if f_poly.degree() > 10:
            return [False, False, False]
            
        r = sp.CRootOf(f_poly, 0)
        facs = sp.factor_list(f_poly, extension=r)[1]
        num_roots = sum(mult for fac, mult in facs if fac.degree() == 1)
        
        neg_q = bool(f_poly.degree() != num_roots)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: L/K is a finite field extension", "H_2: G is the Galois group of L/K", "¬Q: The map is not an isomorphism"]

N_HYP = 2
NEG_Q_INDEX = 2