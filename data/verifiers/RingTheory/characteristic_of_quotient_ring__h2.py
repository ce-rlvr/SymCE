import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
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
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture:
    "If R is a ring with positive characteristic n, then the characteristic of the quotient ring R/I divides n."
    """
    H1 = False
    neg_Q = False
    
    n = None
    m = None
    
    try:
        # 1. Try to unpack as a tuple of integers (char_R, char_R_mod_I)
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int) and isinstance(witness[1], int):
                n, m = witness
                
        # 2. Try to extract from a dictionary
        if isinstance(witness, dict) and n is None:
            n = witness.get('char_R', witness.get('n', witness.get('characteristic')))
            m = witness.get('char_quotient', witness.get('m', witness.get('quotient_characteristic')))
            
        # 3. Try to extract from a custom mock object
        if n is None or m is None:
            n = getattr(witness, 'char_R', getattr(witness, 'n', getattr(witness, 'characteristic', n)))
            m = getattr(witness, 'char_quotient', getattr(witness, 'm', getattr(witness, 'quotient_characteristic', m)))
            
        # 4. Try to extract from a sympy QuotientRing-like object
        if n is None or m is None:
            if hasattr(witness, 'base_ring') and hasattr(witness, 'characteristic'):
                n = getattr(witness.base_ring, 'characteristic', None)
                m = getattr(witness, 'characteristic', None)
                
        # Evaluate the conditions if we successfully extracted the characteristics
        if isinstance(n, int) and isinstance(m, int):
            # H_1: R is a ring with positive characteristic n
            H1 = (n > 0)
            
            # ¬Q: The characteristic of the quotient ring R/I does NOT divide n
            # Note: If m == 0, it does not divide any positive integer n.
            neg_Q = (m == 0 or n % m != 0)
            
    except Exception:
        pass
        
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a ring with positive characteristic n",
    "¬Q: The characteristic of the quotient ring R/I does not divide n"
]

N_HYP = 1
NEG_Q_INDEX = 1