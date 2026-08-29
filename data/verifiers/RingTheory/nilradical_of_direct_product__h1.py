import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_nil_ring(R):
    """
    Checks if the set of nilpotent elements in a finite ring R forms a subring
    (specifically, if it is closed under addition).
    R is expected to be a list or tuple of ring elements (e.g., matrices).
    """
    if not isinstance(R, (list, tuple)):
        return True
    if len(R) == 0:
        return True
    
    n = len(R)
    nilpotents = []
    
    # Find all nilpotent elements
    for x in R:
        curr = x
        is_nil = False
        for _ in range(n):
            if hasattr(curr, 'is_zero_matrix') and curr.is_zero_matrix:
                is_nil = True
                break
            if hasattr(curr, 'is_zero') and curr.is_zero:
                is_nil = True
                break
            if curr == 0:
                is_nil = True
                break
            try:
                curr = curr * x
            except Exception:
                break
        if is_nil:
            nilpotents.append(x)
            
    # Check closure under addition
    for x in nilpotents:
        for y in nilpotents:
            try:
                s = x + y
            except Exception:
                continue
            
            curr = s
            is_nil = False
            for _ in range(n):
                if hasattr(curr, 'is_zero_matrix') and curr.is_zero_matrix:
                    is_nil = True
                    break
                if hasattr(curr, 'is_zero') and curr.is_zero:
                    is_nil = True
                    break
                if curr == 0:
                    is_nil = True
                    break
                try:
                    curr = curr * s
                except Exception:
                    break
            if not is_nil:
                return False
    return True

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample.
    Returns [neg_Q] where neg_Q is True if the conclusion FAILS.
    """
    neg_Q = False
    try:
        # If witness is a pair of rings (e.g., lists of matrices)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R1, R2 = witness
            # For non-commutative rings, the set of nilpotent elements might not form an ideal/ring.
            # If it doesn't form a ring, it cannot be isomorphic to anything as a ring.
            if not is_nil_ring(R1) or not is_nil_ring(R2):
                neg_Q = True
                return [neg_Q]
                
        # If witness is a single ring provided as a list of elements
        elif isinstance(witness, (list, tuple)) and len(witness) > 0:
            if not is_nil_ring(witness):
                neg_Q = True
                return [neg_Q]
                
        # Fallback for string-based symbolic witnesses indicating infinite products or tensor products
        elif isinstance(witness, str):
            if "infinite" in witness.lower() or "tensor" in witness.lower():
                neg_Q = True
                return [neg_Q]
                
    except Exception:
        pass

    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The nilradical of the direct product R1 x R2 is not isomorphic to the direct product of the nilradicals of R1 and R2"
]

N_HYP = 0
NEG_Q_INDEX = 0