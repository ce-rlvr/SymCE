import math
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are commutative rings with identity",
    "H_2: Q_1 is a primary ideal in R_1",
    "¬Q: The ideal Q_1 x R_2 is not a primary ideal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Extract ring sizes (n1, n2) and ideal generators (q1, q2)
        # We model the rings as Z_n1 and Z_n2. n=0 represents the ring of integers Z.
        if isinstance(witness, dict):
            n1 = witness.get('n1')
            n2 = witness.get('n2')
            q1 = witness.get('q1')
            q2 = witness.get('q2', 1)
        elif hasattr(witness, 'n1'):
            n1 = witness.n1
            n2 = witness.n2
            q1 = witness.q1
            q2 = getattr(witness, 'q2', 1)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                n1, n2, q1 = witness
                q2 = 1
            elif len(witness) == 4:
                n1, n2, q1, q2 = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        def extract_n(obj):
            if isinstance(obj, int):
                return obj
            if hasattr(obj, 'order'):
                o = obj.order
                return int(o()) if callable(o) else int(o)
            return int(obj)

        n1 = extract_n(n1)
        n2 = extract_n(n2)
        q1 = int(q1)
        q2 = int(q2)

        # H_1: R_1 and R_2 are commutative rings with identity
        # Z_n (for n >= 0) are all commutative rings with identity.
        h1 = isinstance(n1, int) and n1 >= 0 and isinstance(n2, int) and n2 >= 0
        if not h1:
            return [False, False, False]

        # H_2: Q_1 is a primary ideal in R_1
        if n1 > 0:
            q1_eff = math.gcd(q1, n1)
        else:
            q1_eff = abs(q1)
            
        if q1_eff == 1:
            h2 = False
        elif q1_eff == 0:
            h2 = True
        else:
            h2 = len(factorint(q1_eff)) == 1

        # ¬Q: The ideal Q_1 x R_2 (or Q_1 x Q_2 if provided) is NOT a primary ideal in R
        if n2 > 0:
            q2_eff = math.gcd(q2, n2)
        else:
            q2_eff = abs(q2)
            
        # An ideal I = Q_1 x Q_2 is primary in R_1 x R_2 iff exactly one of the components 
        # is the whole ring (eff == 1) and the other is a primary ideal.
        if q1_eff == 1 and q2_eff == 1:
            is_primary = False
        elif q1_eff != 1 and q2_eff != 1:
            is_primary = False
        else:
            non_trivial = q1_eff if q2_eff == 1 else q2_eff
            if non_trivial == 0:
                is_primary = True
            else:
                is_primary = len(factorint(non_trivial)) == 1
                
        neg_q = not is_primary

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]