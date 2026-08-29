import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        # Since SymPy does not have a built-in representation for arbitrary (e.g. infinite) 
        # field extensions, we expect the witness to be a dictionary, an object with 
        # boolean attributes, or a tuple representing the properties of the extension.
        if isinstance(witness, dict):
            is_galois = witness.get('is_Galois', witness.get('is_galois', False))
            is_normal = witness.get('is_normal', False)
            is_separable = witness.get('is_separable', False)
        elif hasattr(witness, 'is_Galois') or hasattr(witness, 'is_galois') or hasattr(witness, 'is_normal'):
            is_galois = getattr(witness, 'is_Galois', getattr(witness, 'is_galois', False))
            is_normal = getattr(witness, 'is_normal', False)
            is_separable = getattr(witness, 'is_separable', False)
        elif isinstance(witness, tuple) and len(witness) == 3:
            is_galois, is_normal, is_separable = witness
        else:
            return [False]
            
        is_galois = bool(is_galois)
        is_normal = bool(is_normal)
        is_separable = bool(is_separable)
        
        # Conclusion: K/F is a Galois extension if and only if K/F is both normal and separable
        q = (is_galois == (is_normal and is_separable))
        
        # The negated conclusion is True when the equivalence fails
        neg_q = not q
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: K/F is not Galois iff it is both normal and separable"
]

N_HYP = 0
NEG_Q_INDEX = 0