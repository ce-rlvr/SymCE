import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

try:
    from sympy.combinatorics.free_groups import free_group
    Z_group, _ = free_group('x')
except ImportError:
    Z_group = "Z"

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
    A, B = None, None
    if isinstance(witness, dict):
        A = witness.get('A')
        B = witness.get('B')
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 2:
            A = witness[0]
            B = witness[1]
    elif hasattr(witness, 'A') and hasattr(witness, 'B'):
        A = witness.A
        B = witness.B
    
    if A is None or B is None:
        return [False, False, False]

    # H1: B is an infinite group
    h1 = False
    try:
        if hasattr(B, 'order'):
            try:
                if B.order() == sympy.oo:
                    h1 = True
            except Exception:
                pass
        if not h1 and hasattr(B, 'is_infinite'):
            try:
                if B.is_infinite:
                    h1 = True
            except Exception:
                pass
        if not h1 and type(B).__name__ == 'FreeGroup':
            h1 = len(B.generators) > 0
        if not h1 and type(B).__name__ == 'FpGroup':
            if len(B.relators) == 0 and len(B.generators) > 0:
                h1 = True
        if not h1 and B is sympy.S.Integers:
            h1 = True
        if not h1 and isinstance(B, str) and B.lower() in ['z', 'integers', 'infinite cyclic group', 'freegroup']:
            h1 = True
    except Exception:
        h1 = False

    # H2: W is the restricted wreath product of A by B
    # This is definitional for W given A and B.
    h2 = True

    # neg_Q: The center of W is NOT the trivial subgroup
    # Z(A wr B) is non-trivial iff A is trivial and Z(B) is non-trivial
    neg_q = False
    try:
        # Check if A is trivial
        a_trivial = False
        if hasattr(A, 'order'):
            try:
                if A.order() == 1:
                    a_trivial = True
            except Exception:
                pass
        if not a_trivial and hasattr(A, 'is_trivial'):
            try:
                if A.is_trivial:
                    a_trivial = True
            except Exception:
                pass
        if not a_trivial and hasattr(A, 'elements'):
            try:
                if len(list(A.elements)) == 1:
                    a_trivial = True
            except Exception:
                pass
        if not a_trivial and isinstance(A, str) and A.lower() in ['trivial', 'z1', 'c1', '1']:
            a_trivial = True
            
        # Check if Z(B) is non-trivial
        z_b_nontrivial = False
        if type(B).__name__ == 'FreeGroup':
            z_b_nontrivial = (len(B.generators) == 1)
        elif type(B).__name__ == 'FpGroup':
            if len(B.relators) == 0 and len(B.generators) == 1:
                z_b_nontrivial = True
        elif B is sympy.S.Integers:
            z_b_nontrivial = True
        elif isinstance(B, str) and B.lower() in ['z', 'integers', 'infinite cyclic group']:
            z_b_nontrivial = True
        elif hasattr(B, 'center'):
            try:
                C = B.center()
                if hasattr(C, 'order'):
                    z_b_nontrivial = (C.order() > 1)
                elif hasattr(C, 'elements'):
                    z_b_nontrivial = (len(list(C.elements)) > 1)
            except Exception:
                pass
                
        if a_trivial and z_b_nontrivial:
            neg_q = True
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is an infinite group",
    "H_2: W is the restricted wreath product of A by B",
    "¬Q: The center of W is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2