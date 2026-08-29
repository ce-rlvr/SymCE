import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: n is a non-negative integer",
    "¬Q: (G x H)^{(n)} is not equal to G^{(n)} x H^{(n)}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            n = witness['n']
        else:
            G, H, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 0
    except Exception:
        h1 = False
        
    try:
        def derived_n(grp, k):
            ds = grp.derived_series()
            if k < len(ds):
                return ds[k]
            return ds[-1]
        
        GxH = G * H
        GxH_n = derived_n(GxH, n)
        
        G_n = derived_n(G, n)
        H_n = derived_n(H, n)
        Gn_x_Hn = G_n * H_n
        
        if GxH_n.order() != Gn_x_Hn.order():
            is_eq = False
        else:
            try:
                is_eq = GxH_n.is_subgroup(Gn_x_Hn)
            except Exception:
                is_eq = False
                
        neg_q = not is_eq
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]