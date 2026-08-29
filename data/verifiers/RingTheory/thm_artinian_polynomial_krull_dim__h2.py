import sympy
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ, RR, CC, Domain

# Setup standard rings for witnesses
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
ZZ_xy = ZZ.poly_ring(x, y)
QQ_xy = QQ.poly_ring(x, y)

def conditions(witness):
    # H_1: R is a non-zero commutative ring
    try:
        h1 = isinstance(witness, Domain)
    except Exception:
        h1 = False

    # neg_Q: The Krull dimension of the polynomial ring over R is not exactly 1
    try:
        def krull_dim(R):
            if hasattr(R, 'is_Field') and R.is_Field:
                return 0
            if R == ZZ:
                return 1
            if R in (QQ, RR, CC):
                return 0
            
            name = R.__class__.__name__
            if 'IntegerRing' in name:
                return 1
            if 'RationalField' in name or 'RealField' in name or 'ComplexField' in name:
                return 0
            if name == 'PolynomialRing':
                return krull_dim(R.domain) + len(R.symbols)
            if name == 'FractionField':
                return 0
                
            raise ValueError("Unknown ring")
        
        dim_R = krull_dim(witness)
        dim_Rx = dim_R + 1
        neg_q = (dim_Rx != 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a non-zero commutative ring",
    "neg_Q: The Krull dimension of the polynomial ring over R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1