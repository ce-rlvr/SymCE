import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        a = int(witness)
    except Exception:
        return [False]
        
    try:
        m = a**3 + a + 1
        val = a**2 + 1
        
        try:
            # In Python, pow(base, -1, mod) computes the modular inverse.
            # It raises a ValueError if the inverse does not exist (e.g., m=1, m=-1, or gcd != 1).
            inv = pow(val, -1, m)
            concl = (inv % m) == ((-a) % m)
        except ValueError:
            # If the modular inverse does not exist, the conclusion fails.
            concl = False
            
        neg_Q = not concl
    except Exception:
        neg_Q = True
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of a^2+1 modulo a^3+a+1 is not congruent to -a mod (a^3+a+1)"
]
N_HYP = 0
NEG_Q_INDEX = 0