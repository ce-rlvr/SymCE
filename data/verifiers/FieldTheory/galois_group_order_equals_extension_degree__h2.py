import sympy
from sympy import Poly, factor_list, RootOf, sqrt
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                poly, G = witness
            elif len(witness) == 3:
                poly, _, G = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        if hasattr(poly, 'free_symbols'):
            syms = poly.free_symbols
            var = list(syms)[0] if len(syms) == 1 else x
        else:
            var = x
        p = Poly(poly, var, domain='QQ')
        h1 = p.is_irreducible and p.degree() >= 1
    except Exception:
        h1 = False
        
    try:
        deg = p.degree()
        if hasattr(G, 'order'):
            order_G = G.order()
        else:
            order_G = int(G)
            
        if deg == 1:
            is_gal = True
        elif deg == 2:
            is_gal = True
        elif deg == 3:
            disc = p.discriminant()
            is_gal = sqrt(disc).is_rational
        else:
            r = RootOf(poly, 0)
            factors = factor_list(poly, extension=r)[1]
            is_gal = all(Poly(fac, var).degree() == 1 for fac, mult in factors)
            
        q = (is_gal == (order_G == deg))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = ["H_1: L is a finite field extension of K", "¬Q: L is Galois over K is not equivalent to order of G equals degree"]
N_HYP = 1
NEG_Q_INDEX = 1