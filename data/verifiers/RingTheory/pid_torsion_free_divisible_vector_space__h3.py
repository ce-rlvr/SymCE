import sympy
from sympy import ZZ, QQ, Symbol, eye, zeros
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

try:
    QQ_x = QQ[x]
except Exception:
    QQ_x = None

try:
    QQ_frac = QQ.frac_field(x)
except Exception:
    QQ_frac = None

def conditions(witness):
    h1 = h2 = h3 = h4 = neg_q = False

    # 1. Check if witness is a dictionary
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('R_is_PID', False))
            h2 = bool(witness.get('K_is_frac_field', False))
            h3 = bool(witness.get('M_is_torsion_free', False))
            h4 = bool(witness.get('M_is_divisible', False))
            neg_q = not bool(witness.get('admits_unique_K_vector_space_structure', True))
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    # 2. Check if witness is an object with attributes
    if hasattr(witness, 'R_is_PID'):
        try:
            h1 = bool(getattr(witness, 'R_is_PID', False))
            h2 = bool(getattr(witness, 'K_is_frac_field', False))
            h3 = bool(getattr(witness, 'M_is_torsion_free', False))
            h4 = bool(getattr(witness, 'M_is_divisible', False))
            neg_q = not bool(getattr(witness, 'admits_unique_K_vector_space_structure', True))
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    # 3. Check if witness is a tuple (R, K, M)
    if isinstance(witness, tuple) and len(witness) == 3:
        try:
            R, K, M = witness
            
            # H1: R is a PID
            try:
                if R in (ZZ, QQ):
                    h1 = True
                elif QQ_x is not None and R == QQ_x:
                    h1 = True
                elif hasattr(R, 'is_PID'):
                    h1 = bool(R.is_PID)
                else:
                    h1 = False
            except Exception:
                h1 = False
                
            # H2: K is the field of fractions of R
            try:
                if R == ZZ and K == QQ:
                    h2 = True
                elif R == QQ and K == QQ:
                    h2 = True
                elif QQ_x is not None and QQ_frac is not None and R == QQ_x and K == QQ_frac:
                    h2 = True
                elif hasattr(R, 'frac_field'):
                    h2 = (K == R.frac_field)
                else:
                    h2 = False
            except Exception:
                h2 = False
                
            # H3: M is torsion-free
            try:
                if M in (ZZ, QQ):
                    h3 = True
                elif hasattr(M, 'is_torsion_free'):
                    h3 = bool(M.is_torsion_free)
                else:
                    h3 = False
            except Exception:
                h3 = False
                
            # H4: M is divisible
            try:
                if M == QQ:
                    h4 = True
                elif M == ZZ:
                    h4 = False
                elif hasattr(M, 'is_divisible'):
                    h4 = bool(M.is_divisible)
                else:
                    h4 = False
            except Exception:
                h4 = False
                
            # neg_Q: M does NOT admit a unique K-vector space structure extending its R-module structure
            try:
                if M == QQ and R not in (ZZ, QQ):
                    neg_q = True
                elif hasattr(witness, 'admits_unique_K_vector_space_structure'):
                    neg_q = not bool(witness.admits_unique_K_vector_space_structure())
                else:
                    neg_q = False
            except Exception:
                neg_q = False
                
        except Exception:
            pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: K is the field of fractions of R",
    "H_3: M is torsion-free",
    "H_4: M is divisible",
    "¬Q: M does not admit a unique K-vector space structure extending its R-module structure"
]

N_HYP = 4
NEG_Q_INDEX = 4