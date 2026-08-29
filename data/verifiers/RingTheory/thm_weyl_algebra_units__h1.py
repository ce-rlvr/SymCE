import sympy
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
x, y, t, d = sympy.symbols('x y t d')

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
    Checks if the witness is a valid counterexample to the false conjecture:
    "The group of units of A_1(K) is exactly K^\\times"
    
    The true theorem requires K to be a reduced ring (or a domain/field).
    If K is not reduced (e.g., Z/4Z), A_1(K) has units not in K^\\times.
    """
    h1 = False
    neg_q = False
    
    try:
        # 1. Witness is an integer n (representing the ring Z/nZ)
        n = None
        if isinstance(witness, int):
            n = witness
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            n = int(witness)
        elif isinstance(witness, tuple) and len(witness) > 0:
            if isinstance(witness[0], int):
                n = witness[0]
            elif hasattr(witness[0], 'is_Integer') and witness[0].is_Integer:
                n = int(witness[0])
                
        if n is not None:
            n = abs(n)
            if n >= 2:
                h1 = True
                factors = factorint(n)
                # A_1(Z/nZ) has extra units iff Z/nZ is not reduced (n is not square-free)
                neg_q = any(v >= 2 for v in factors.values())
            elif n == 0:
                # Z or Q
                h1 = True
                neg_q = False
            return [h1, neg_q]
            
        # 2. Witness is a string representing a ring like "Z/4Z"
        if isinstance(witness, str):
            digits = ''.join(c for c in witness if c.isdigit())
            if digits:
                n = int(digits)
                if n >= 2:
                    h1 = True
                    factors = factorint(n)
                    neg_q = any(v >= 2 for v in factors.values())
                    return [h1, neg_q]
                    
        # 3. Witness is a tuple (Symbol, k) representing K[t]/(t^k)
        if isinstance(witness, tuple) and len(witness) >= 2:
            if isinstance(witness[0], sympy.Symbol) and isinstance(witness[1], int):
                h1 = True
                neg_q = (witness[1] >= 2)
                return [h1, neg_q]
                
        # 4. Witness is a matrix ring (which has zero divisors and nilpotents)
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            if witness.shape[0] >= 2 and witness.shape[1] >= 2:
                h1 = True
                neg_q = True
                return [h1, neg_q]
                
        # 5. Witness is a sympy field or domain (reduced rings)
        if hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
            neg_q = False
            return [h1, neg_q]
            
        if hasattr(witness, 'is_Domain') and witness.is_Domain:
            h1 = True
            neg_q = False
            return [h1, neg_q]
            
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: K is a valid ring for the Weyl algebra",
    "¬Q: The group of units of A_1(K) is not exactly K^\\times"
]

N_HYP = 1
NEG_Q_INDEX = 1