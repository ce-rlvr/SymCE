import sympy
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

# Provide some standard rings that might be used as witnesses
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
ZZ_x_y = ZZ.poly_ring(x, y)
QQ_x_y = QQ.poly_ring(x, y)

def get_global_dimension(R):
    """
    Helper function to compute the global dimension of standard sympy domains.
    """
    # Fields have global dimension 0
    if getattr(R, 'is_Field', False):
        return 0
    
    name = R.__class__.__name__
    
    # Z has global dimension 1
    if name == 'IntegerRing':
        return 1
    
    # Fallback for some fields just in case is_Field is missing
    if name in ('RationalField', 'RealField', 'ComplexField', 'AlgebraicField', 'GaloisField'):
        return 0
    
    # Polynomial rings R[x_1, ..., x_n] have global dimension = gl_dim(R) + n
    if hasattr(R, 'domain'):
        gens = getattr(R, 'symbols', getattr(R, 'gens', None))
        if gens is not None:
            base_dim = get_global_dimension(R.domain)
            return base_dim + len(gens)
            
    raise ValueError(f"Cannot determine global dimension for {R}")

def conditions(witness) -> list[bool]:
    # H_1: R is not a field.
    try:
        is_field = getattr(witness, 'is_Field', None)
        if is_field is None:
            h1_ok = False
        else:
            h1_ok = not bool(is_field)
    except Exception:
        h1_ok = False

    # ¬Q: The global dimension of R is NOT exactly 1.
    try:
        dim = get_global_dimension(witness)
        neg_q_ok = (dim != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is not a field",
    "¬Q: The global dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1