import sympy
from sympy import QQ, ZZ
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (F, n) where F is a sympy Domain (e.g., QQ, ZZ)
    and n is the dimension of the vector space, or simply an integer n (assuming a field like QQ).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, n = witness
            
            if isinstance(F, str):
                if F == 'QQ':
                    F = QQ
                elif F == 'ZZ':
                    F = ZZ
            
            is_field = False
            if hasattr(F, 'is_Field'):
                is_field = bool(F.is_Field)
            elif hasattr(F, 'is_field'):
                is_field = bool(F.is_field)
                
            if isinstance(n, int) and n >= 0:
                h1 = is_field
                
            if isinstance(n, int) and n >= 1:
                h2 = True
                
            if isinstance(n, int) and n >= 1:
                # GL(n, F) acts transitively on F^n \ {0} if and only if F is a field.
                # If F is not a field, the action is not transitive.
                neg_q = not is_field
                
        elif isinstance(witness, int):
            n = witness
            is_field = True  # Assume a standard field like QQ or RR if only dimension is given
            if n >= 0:
                h1 = True
            if n >= 1:
                h2 = True
                neg_q = False
                
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: The dimension of V is at least 1",
    "¬Q: The natural action of GL(V) on the set of non-zero vectors V \\setminus \\{0\\} is not transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2