import sympy
from sympy.abc import x, y
from sympy import Poly
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices

# Top-level setup
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, f = witness
        else:
            R = sympy.S.Integers
            f = witness
            
        # H1: R is a commutative ring
        if R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = R.is_commutative is not False
        else:
            h1 = True
            
        # neg_Q: R(x,y)/<y - f> is not isomorphic to R(x)
        g = y - f
        
        is_iso = False
        if g != 0:
            try:
                p = Poly(g, x, y)
                deg_y = p.degree(y)
                deg_x = p.degree(x)
                
                if deg_y == 1:
                    py = Poly(g, y)
                    lc = py.LC()
                    if lc in [1, -1]:
                        is_iso = True
                        
                if not is_iso and deg_x == 1:
                    px = Poly(g, x)
                    lc = px.LC()
                    if lc in [1, -1]:
                        is_iso = True
            except Exception:
                pass
                
        neg_q = not is_iso
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The factor ring R(x,y)/<y - f> is not isomorphic to R(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1