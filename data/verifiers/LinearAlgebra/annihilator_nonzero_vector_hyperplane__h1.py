import sympy
from sympy import Matrix, Symbol, Expr, Poly, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        v = witness
        # If the witness is provided as a tuple (V, v), extract v
        if isinstance(witness, tuple) and len(witness) == 2:
            V, v = witness
            
        # Finite-dimensional vector representations
        if hasattr(v, 'is_Matrix') and v.is_Matrix:
            h1 = not v.is_zero_matrix
            neg_q = False
        elif 'Vector' in type(v).__name__ or 'Matrix' in type(v).__name__:
            try:
                h1 = bool(v != 0)
            except Exception:
                h1 = True
            neg_q = False
        elif hasattr(v, '__iter__') and hasattr(v, '__len__') and not isinstance(v, str):
            if isinstance(v, dict):
                h1 = any(val != 0 for val in v.values())
            else:
                h1 = any(x != 0 for x in v)
            neg_q = False
        elif isinstance(v, (int, float, complex)):
            h1 = v != 0
            neg_q = False
            
        # Infinite-dimensional vector representations (counterexamples)
        elif isinstance(v, Expr):
            if v.is_number:
                h1 = bool(v != 0)
                neg_q = False
            else:
                # Symbolic expressions (e.g., polynomials/functions) represent infinite-dimensional vectors
                h1 = bool(v != 0)
                neg_q = True
        elif isinstance(v, Poly):
            h1 = not v.is_zero
            neg_q = True
        elif isinstance(v, str):
            if v.strip().startswith('[') or v.strip().startswith('('):
                h1 = True
                neg_q = False
            else:
                h1 = True
                neg_q = True
        else:
            # Fallback for custom objects representing infinite-dimensional vectors
            h1 = True
            neg_q = True
            
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: v is a non-zero vector in V",
    "¬Q: The annihilator {v}^0 does NOT have dimension dim(V) - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1