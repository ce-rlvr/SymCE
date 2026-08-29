import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # The witness can be a tuple (Ring, Module) or just the Module (assuming Ring is Z)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = Z
            M = witness
            
        if R == Z or R == 'Z':
            if isinstance(M, int):
                # Integer n represents the Z-module Z/nZ
                h1 = True
                # Z/nZ has a projective cover over Z iff it is projective (i.e., n = 1, the zero module)
                neg_q = abs(M) > 1
            elif M == Z:
                # Z is a finitely generated free (hence projective) Z-module
                h1 = True
                neg_q = False
            elif isinstance(M, (list, tuple)) and all(isinstance(x, int) for x in M):
                # List of integers represents a direct sum of cyclic Z-modules
                h1 = True
                neg_q = any(abs(x) > 1 for x in M)
            elif M == Q:
                # Q is not finitely generated over Z
                h1 = False
                neg_q = True
            elif hasattr(M, 'is_abelian'):
                # SymPy finite group interpreted as a Z-module
                if M.is_abelian:
                    h1 = True
                    neg_q = M.order() > 1
            elif isinstance(M, str):
                # String representation fallback
                M_str = M.replace(" ", "").lower()
                if M_str in ["z/2z", "z2", "z_2", "z/3z", "z3", "z_3", "z/4z", "z4", "z_4"]:
                    h1 = True
                    neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated right R-module",
    "¬Q: M does not have a projective cover"
]

N_HYP = 1
NEG_Q_INDEX = 1