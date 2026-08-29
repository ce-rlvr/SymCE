import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: M_1, M_2, ..., M_n is a finite collection of Artinian R-modules",
    "¬Q: The direct sum of M_1, M_2, ..., M_n is not an Artinian R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_artinian(m):
    """
    Helper to check if a module representation is Artinian.
    We interpret non-negative integers as finite lengths/dimensions of modules,
    and finite groups as finite (hence Artinian) Z-modules.
    """
    if isinstance(m, (int, float)):
        return 0 <= m < oo
    if m == oo:
        return False
    if hasattr(m, 'order'):
        try:
            return m.order() < oo
        except Exception:
            return False
    return False

def conditions(witness) -> list[bool]:
    try:
        # The witness should be a finite collection (list or tuple) of modules
        if not isinstance(witness, (list, tuple)):
            return [False, False]
        
        # H_1: All modules in the finite collection are Artinian
        h1 = all(is_artinian(m) for m in witness)
        
        # ¬Q: The direct sum of the collection is NOT an Artinian R-module.
        # A finite direct sum of modules is Artinian if and only if 
        # each of the individual modules is Artinian.
        is_sum_artinian = all(is_artinian(m) for m in witness)
        neg_q = not is_sum_artinian
        
        return [h1, neg_q]
    except Exception:
        return [False, False]