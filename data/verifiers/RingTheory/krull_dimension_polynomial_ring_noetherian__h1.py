import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def _extract_properties(witness):
    is_noeth = None
    d = None
    poly_d = None
    
    if isinstance(witness, dict):
        is_noeth = witness.get('is_noetherian', witness.get('noetherian', witness.get('is_Noetherian')))
        d = witness.get('krull_dimension', witness.get('dim', witness.get('d')))
        poly_d = witness.get('poly_ring_krull_dimension', witness.get('dim_poly', witness.get('poly_dim', witness.get('dim_Rx'))))
    elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
        is_noeth = witness[0]
        d = witness[1]
        poly_d = witness[2]
    else:
        is_noeth = getattr(witness, 'is_noetherian', getattr(witness, 'noetherian', getattr(witness, 'is_Noetherian', None)))
        d = getattr(witness, 'krull_dimension', getattr(witness, 'dim', getattr(witness, 'd', None)))
        poly_d = getattr(witness, 'poly_ring_krull_dimension', getattr(witness, 'dim_poly', getattr(witness, 'poly_dim', getattr(witness, 'dim_Rx', None))))
        
    if callable(is_noeth):
        try:
            is_noeth = is_noeth()
        except Exception:
            pass
    if callable(d):
        try:
            d = d()
        except Exception:
            pass
    if callable(poly_d):
        try:
            poly_d = poly_d()
        except Exception:
            pass
            
    return is_noeth, d, poly_d

def conditions(witness) -> list[bool]:
    is_noeth, d, poly_d = _extract_properties(witness)
    
    try:
        h1 = bool(is_noeth) if is_noeth is not None else False
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(d, int) and not isinstance(d, bool)
    except Exception:
        h2 = False
        
    try:
        if h2 and poly_d is not None:
            neg_q = (poly_d != d + 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The ring R is Noetherian",
    "H_2: The Krull dimension of R is a finite integer d",
    "¬Q: The Krull dimension of the polynomial ring is not exactly d + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2