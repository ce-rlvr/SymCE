import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

ZZ = sympy.ZZ
QQ = sympy.QQ

def is_ring(R):
    if str(R) in ['Z', 'ZZ', 'ZZ()', 'Q', 'QQ', 'QQ()', 'R', 'C']:
        return True
    try:
        if getattr(R, 'is_Ring', False) or getattr(R, 'is_Field', False):
            return True
    except Exception:
        pass
    try:
        from sympy.polys.domains.ring import Ring
        from sympy.polys.domains.field import Field
        if isinstance(R, (Ring, Field)):
            return True
    except Exception:
        pass
    return False

def is_artinian_module(R, M):
    R_str = str(R)
    M_str = str(M)
    
    # Check for Z-modules (abelian groups)
    if R_str in ['Z', 'ZZ', 'ZZ()']:
        # Finite abelian groups are Artinian Z-modules
        if hasattr(M, 'is_abelian') and M.is_abelian:
            try:
                if M.order() < float('inf'):
                    return True
            except Exception:
                pass
        # Z and Q are not Artinian Z-modules
        if M_str in ['Z', 'ZZ', 'ZZ()', 'Q', 'QQ', 'QQ()', 'Integers', 'Reals', 'Complexes']:
            return False
            
    # Check for Q-modules (vector spaces over Q)
    if R_str in ['Q', 'QQ', 'QQ()']:
        # Q is a 1-dimensional (hence Artinian) Q-module
        if M_str in ['Q', 'QQ', 'QQ()']:
            return True
        # Z is not a Q-module, Q[x] is not Artinian
        if M_str in ['Z', 'ZZ', 'ZZ()', 'Q[x]']:
            return False
            
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, M, N) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
            N = witness.get('N')
        else:
            R, M, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a ring
    try:
        h1 = is_ring(R)
    except Exception:
        h1 = False
        
    # H_2: M is an Artinian R-module
    try:
        h2 = is_artinian_module(R, M)
    except Exception:
        h2 = False
        
    # ¬Q: N is NOT an Artinian R-module
    try:
        neg_q = not is_artinian_module(R, N)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is an Artinian R-module",
    "¬Q: N is not an Artinian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2