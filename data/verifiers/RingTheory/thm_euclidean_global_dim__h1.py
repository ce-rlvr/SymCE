import sympy
from sympy import S
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ, RR, CC

# Standard ring bindings for potential witnesses
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
QQ_x_y = QQ.poly_ring(x, y)
ZZ_x_y = ZZ.poly_ring(x, y)
QQ_x_y_z = QQ.poly_ring(x, y, z)
ZZ_x_y_z = ZZ.poly_ring(x, y, z)

def is_field(R):
    if hasattr(R, 'is_Field'):
        return bool(R.is_Field)
    if R in (S.Rationals, S.Reals, S.Complexes):
        return True
    if R == S.Integers:
        return False
    name = R.__class__.__name__
    if name in ('RationalField', 'GMPYRationalField', 'PythonRationalField', 'RealField', 'ComplexField'):
        return True
    if 'Frac' in name:
        return True
    return False

def get_global_dimension(R):
    if is_field(R):
        return 0
    if R in (S.Integers, ZZ):
        return 1
    name = R.__class__.__name__
    if name in ('IntegerRing', 'GMPYIntegerRing', 'PythonIntegerRing'):
        return 1
    
    if 'Poly' in name:
        base = getattr(R, 'domain', getattr(R, 'dom', None))
        gens = getattr(R, 'gens', getattr(R, 'symbols', []))
        if base is not None:
            return get_global_dimension(base) + len(gens)
            
    raise ValueError(f"Cannot determine global dimension for {R}")

def conditions(witness) -> list[bool]:
    try:
        h1 = not is_field(witness)
    except Exception:
        h1 = False

    try:
        dim = get_global_dimension(witness)
        neg_q = (dim != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is not a field",
    "¬Q: The global homological dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1