import sympy as sp
from sympy.polys.polytools import Poly
from sympy.abc import x

# Top-level setup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        if hasattr(witness, 'free_symbols') and x not in witness.free_symbols and not isinstance(witness, Poly):
            poly = sp.minpoly(witness, x, polys=True)
        else:
            poly = Poly(witness, x, domain='QQ')
            
        factors = poly.factor_list()[1]
        
        for factor, mult in factors:
            deg = factor.degree()
            if deg == 1 or deg == 2:
                h1_ok = True
                break
            if (deg & (deg - 1)) == 0:
                try:
                    grp = factor.galois_group()
                    order = grp.order()
                    if (order & (order - 1)) == 0:
                        h1_ok = True
                        break
                except Exception:
                    pass
    except Exception:
        h1_ok = False

    try:
        if hasattr(witness, 'free_symbols') and x not in witness.free_symbols and not isinstance(witness, Poly):
            poly = sp.minpoly(witness, x, polys=True)
        else:
            poly = Poly(witness, x, domain='QQ')
            
        factors = poly.factor_list()[1]
        
        is_2_group = True
        for factor, mult in factors:
            deg = factor.degree()
            if deg <= 1:
                continue
            
            if (deg & (deg - 1)) != 0:
                is_2_group = False
                break
                
            try:
                grp = factor.galois_group()
                order = grp.order()
                if (order & (order - 1)) != 0:
                    is_2_group = False
                    break
            except Exception:
                pass
                
        neg_q_ok = not is_2_group
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: alpha is constructible",
    "not Q: degree is not a power of 2"
]

N_HYP = 1
NEG_Q_INDEX = 1