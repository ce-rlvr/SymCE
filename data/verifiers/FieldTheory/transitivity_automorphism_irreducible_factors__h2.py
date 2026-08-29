import sympy
from sympy import Poly, factor_list
from sympy.abc import x, y

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            g = witness.get('g', x)
            f = witness.get('f', x)
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            g, f = witness
        else:
            g = x
            f = witness
            
        g = sympy.sympify(g)
        f = sympy.sympify(f)
        
        g_poly = Poly(g, x, domain='QQ')
        f_poly = Poly(f, x, domain='QQ')
        
        if g_poly.degree() < 1:
            return [False, False]
            
        if not g_poly.is_irreducible:
            h1 = False
        else:
            deg = g_poly.degree()
            if deg == 1 or deg == 2:
                h1 = True
            elif deg > 6:
                h1 = False
            else:
                from sympy import RootOf
                r = RootOf(g_poly, 0)
                factors = factor_list(g_poly, extension=r)[1]
                h1 = all(Poly(fac, x).degree() == 1 for fac, mult in factors)
                
        f_factors = factor_list(f_poly)[1]
        num_distinct_factors = len(f_factors)
        
        neg_q = (num_distinct_factors > 1)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: E/F is a normal field extension", "\xacQ: Aut(E/F) does not act transitively"]
N_HYP = 1
NEG_Q_INDEX = 1