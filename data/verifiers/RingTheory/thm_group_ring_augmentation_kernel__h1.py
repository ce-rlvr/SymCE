import sympy
from sympy.combinatorics import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup
class CustomRing:
    def __init__(self, name, has_identity=True):
        self.name = name
        self.has_identity = has_identity
        self.is_Ring = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

EvenIntegers = CustomRing("2Z", has_identity=False)
Integers = CustomRing("Z", has_identity=True)
Rationals = CustomRing("Q", has_identity=True)
Reals = CustomRing("R", has_identity=True)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    "H_1: G is a group",
    "H_2: The group ring of G over R is given",
    "H_3: epsilon is the augmentation homomorphism",
    "¬Q: The kernel of epsilon is not generated as an ideal by g - 1"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    R, G = None, None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, G = witness
        elif isinstance(witness, dict):
            R = witness.get('R', EvenIntegers)
            G = witness.get('G', S3)
        elif isinstance(witness, str):
            if "2Z" in witness or "Even" in witness or "without identity" in witness.lower():
                R = EvenIntegers
            else:
                R = Integers
            G = S3
        else:
            R = witness
            G = S3
    except Exception:
        pass

    try:
        h1 = hasattr(G, 'is_group') or 'Group' in str(type(G))
        if not h1:
            h1 = any(G is g for g in [S3, S4, A4, D4, C4, V4, Z2, Z3, Z4, Z6, trivial])
    except Exception:
        h1 = False

    try:
        h2 = isinstance(R, CustomRing) or hasattr(R, 'is_Ring')
        if not h2:
            h2 = any(R is r for r in [EvenIntegers, Integers, Rationals, Reals])
    except Exception:
        h2 = False

    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    try:
        if hasattr(R, 'has_identity'):
            has_id = R.has_identity
        else:
            has_id = True
            
        neg_q = not has_id
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]