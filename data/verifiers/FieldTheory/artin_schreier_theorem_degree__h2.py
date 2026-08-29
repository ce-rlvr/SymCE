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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: C is an algebraically closed field",
    "H_2: The degree of the field extension C over R is finite",
    "H_3: R is not equal to C",
    "¬Q: The degree of the field extension C over R is not exactly 2"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if witness == sympy.oo or witness == float('inf'):
            return [True, False, True, True]

        # 1. Witness is a dictionary containing properties
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_algebraically_closed', True))
            deg = witness.get('degree', witness.get('index', 1))
            h2 = deg != float('inf') and deg != sympy.oo
            h3 = deg > 1
            neg_q = deg != 2
            return [h1, h2, h3, neg_q]
            
        # 2. Witness is a Galois group (e.g., a SymPy permutation group)
        if hasattr(witness, 'order') and callable(witness.order):
            deg = witness.order()
            h1 = True
            h2 = deg != float('inf') and deg != sympy.oo
            h3 = deg > 1
            neg_q = deg != 2
            return [h1, h2, h3, neg_q]
            
        # 3. Witness is an object with a degree attribute
        if hasattr(witness, 'degree'):
            h1 = bool(getattr(witness, 'is_algebraically_closed', True))
            deg = witness.degree
            if callable(deg):
                deg = deg()
            h2 = deg != float('inf') and deg != sympy.oo
            h3 = deg > 1
            neg_q = deg != 2
            return [h1, h2, h3, neg_q]
            
        # 4. Witness is a number representing the degree C over R
        if isinstance(witness, (int, float)) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            deg = int(witness)
            h1 = True
            h2 = True
            h3 = deg > 1
            neg_q = deg != 2
            return [h1, h2, h3, neg_q]
            
        # 5. Witness is a string representing the degree
        if isinstance(witness, str) and witness.isdigit():
            deg = int(witness)
            h1 = True
            h2 = True
            h3 = deg > 1
            neg_q = deg != 2
            return [h1, h2, h3, neg_q]
            
        # 6. Witness is a tuple/list where the first element is the degree
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            if isinstance(witness[0], (int, float)) or (hasattr(witness[0], 'is_Integer') and witness[0].is_Integer):
                deg = int(witness[0])
                h1 = True
                h2 = True
                h3 = deg > 1
                neg_q = deg != 2
                return [h1, h2, h3, neg_q]
                
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]