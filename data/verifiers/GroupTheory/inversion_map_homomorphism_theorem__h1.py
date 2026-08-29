import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_1: G is a set with an inversion map f(x) = x^-1",
    "¬Q: f is a homomorphism iff G is abelian is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # H_1: G is a set with an inversion map f(x) = x^-1
    h1_ok = False
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
        elif hasattr(witness, 'generate'):
            elements = list(witness.generate())
        else:
            elements = list(witness)
            
        if elements:
            h1_ok = True
            for x in elements:
                inv = x**-1
                if inv not in elements:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # ¬Q: f is a homomorphism iff G is abelian is FALSE
    neg_q_ok = False
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
        elif hasattr(witness, 'generate'):
            elements = list(witness.generate())
        else:
            elements = list(witness)
            
        is_homo = True
        for x in elements:
            for y in elements:
                if (x * y)**-1 != (x**-1) * (y**-1):
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if hasattr(witness, 'is_abelian'):
            is_abelian = bool(witness.is_abelian)
        else:
            is_abelian = True
            for x in elements:
                for y in elements:
                    if x * y != y * x:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
                    
        neg_q_ok = (is_homo != is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]