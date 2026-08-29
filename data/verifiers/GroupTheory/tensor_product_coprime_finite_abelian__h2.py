import math
import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a finite abelian group of order m",
    "H_2: m and n are coprime integers",
    "¬Q: The tensor product A \\otimes_\\mathbb{Z} B is not the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            m = witness.get('m')
            n = witness.get('n')
        else:
            A, B, m, n = witness
    except Exception:
        return [False, False, False]
    
    # H1: A is a finite abelian group of order m
    try:
        if hasattr(A, 'is_abelian') and hasattr(A, 'order'):
            h1 = bool(A.is_abelian) and (int(A.order()) == int(m))
        elif isinstance(A, list):
            h1 = all(isinstance(x, (int, sympy.Integer)) and int(x) > 0 for x in A) and math.prod(int(x) for x in A) == int(m)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: m and n are coprime integers
    try:
        h2 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and math.gcd(int(m), int(n)) == 1
    except Exception:
        h2 = False

    # neg_Q: A \otimes B is NOT the trivial group
    try:
        is_trivial = True
        
        # Determine the order of A
        if hasattr(A, 'order'):
            order_A = int(A.order())
        elif isinstance(A, list):
            order_A = math.prod(int(x) for x in A)
        else:
            order_A = 1
            
        # Check triviality of the tensor product A \otimes B
        # For finite abelian A, A \otimes B is trivial iff gcd(|A|, |B_ab|) == 1
        if hasattr(B, 'order') and hasattr(B, 'derived_subgroup'):
            order_B_ab = int(B.order()) // int(B.derived_subgroup().order())
            is_trivial = (math.gcd(order_A, order_B_ab) == 1)
        elif isinstance(B, list):
            # B given as a list of invariant factors (0 means Z)
            is_trivial = all(math.gcd(order_A, int(b)) == 1 for b in B)
        elif isinstance(B, (int, sympy.Integer)):
            # B given as a single invariant factor (e.g., 0 for Z, k for Z_k)
            B_int = int(B)
            if B_int == 0:
                is_trivial = (order_A == 1)
            else:
                is_trivial = (math.gcd(order_A, B_int) == 1)
        else:
            # Unrecognized format for B, cannot evaluate
            return [h1, h2, False]
            
        neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]