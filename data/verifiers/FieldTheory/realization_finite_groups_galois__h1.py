import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    """
    Check if the witness is a counterexample to the false conjecture:
    "There exists a field F and a finite Galois extension E of F such that 
    the Galois group Gal(E/F) is isomorphic to G."
    
    Since every finite group is realizable as a Galois group over some field 
    (and thus over a finite extension), the conclusion fails if and only if 
    G is an infinite group (or not a finite group).
    """
    try:
        is_finite = False
        
        # Check if the witness has a finite order
        if hasattr(witness, 'order'):
            try:
                o = witness.order()
                if o != sympy.oo and o != float('inf'):
                    is_finite = True
            except Exception:
                pass
        
        # Check SymPy's is_finite property
        if not is_finite and hasattr(witness, 'is_finite'):
            try:
                if witness.is_finite is True:
                    is_finite = True
            except Exception:
                pass
                
        # Standard Python finite collections
        if not is_finite and isinstance(witness, (list, set, tuple)):
            is_finite = True
            
        # The conclusion fails if the group is NOT finite
        neg_q = not is_finite
        
    except Exception:
        neg_q = True

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is not realizable as the Galois group of a finite extension (e.g., G is infinite)"
]

N_HYP = 0
NEG_Q_INDEX = 0