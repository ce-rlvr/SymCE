import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient, factorint
from sympy.abc import x, y, z

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

def conditions(witness):
    try:
        # Extract the cardinality q from the witness
        if hasattr(witness, 'order'):
            if callable(witness.order):
                q = int(witness.order())
            else:
                q = int(witness.order)
        elif hasattr(witness, '__len__'):
            q = len(witness)
        else:
            q = int(witness)
    except Exception:
        return [False, False]
        
    try:
        # H_1: F has a well-defined cardinality q (must be positive)
        h1 = (q > 0)
    except Exception:
        h1 = False
        
    try:
        # Determine if the witness is explicitly a field
        is_field = False
        if hasattr(witness, 'is_Field') and getattr(witness, 'is_Field'):
            is_field = True
        elif hasattr(witness, 'is_field') and getattr(witness, 'is_field'):
            is_field = True
            
        # Calculate the actual number of primitive elements
        if is_field:
            # For a finite field, the multiplicative group is cyclic of order q-1
            actual = totient(q - 1) if q - 1 > 0 else 0
        elif q == 1:
            actual = 1
        else:
            # If not explicitly a field, we assume the witness represents the ring Z/qZ.
            # The number of primitive elements is the number of generators of (Z/qZ)^*.
            # (Z/qZ)* is cyclic iff q is 2, 4, p^k, or 2p^k for an odd prime p.
            is_cyclic = False
            if q in (2, 4):
                is_cyclic = True
            else:
                factors = factorint(q)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                    if p > 2:
                        is_cyclic = True
                elif len(factors) == 2:
                    if 2 in factors and factors[2] == 1:
                        is_cyclic = True
            
            if is_cyclic:
                actual = totient(totient(q))
            else:
                actual = 0
                
        # The conclusion claims the number of primitive elements is always ϕ(q-1)
        expected = totient(q - 1) if q - 1 > 0 else 0
        
        # neg_Q is True if the actual number of primitive elements does NOT equal ϕ(q-1)
        neg_q = (actual != expected)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let q be the cardinality of F",
    "¬Q: The number of primitive elements of F is not ϕ(q-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1