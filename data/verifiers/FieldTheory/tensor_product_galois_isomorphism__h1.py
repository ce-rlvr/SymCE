import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Standard group theory and linear algebra objects
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

# Domain-specific objects for Field Theory
class FieldExtension:
    def __init__(self, name, is_galois, is_finite):
        self.name = name
        self.is_galois = is_galois
        self.is_finite = is_finite
        
    def __str__(self):
        return self.name

class GalGroup:
    def __init__(self, ext):
        self.ext = ext

Q_bar_over_Q = FieldExtension("Q_bar/Q", True, False)
Q_sqrt_2_over_Q = FieldExtension("Q(sqrt(2))/Q", True, True)
C_over_R = FieldExtension("C/R", True, True)
Fp_bar_over_Fp = FieldExtension("Fp_bar/Fp", True, False)
Q_pi_over_Q = FieldExtension("Q(pi)/Q", False, False)
Q_cbrt_2_over_Q = FieldExtension("Q(cbrt(2))/Q", False, True)

G_Q_bar_over_Q = GalGroup(Q_bar_over_Q)
G_Q_sqrt_2_over_Q = GalGroup(Q_sqrt_2_over_Q)
G_C_over_R = GalGroup(C_over_R)
G_Fp_bar_over_Fp = GalGroup(Fp_bar_over_Fp)
G_Q_pi_over_Q = GalGroup(Q_pi_over_Q)
G_Q_cbrt_2_over_Q = GalGroup(Q_cbrt_2_over_Q)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            ext, G = witness
        else:
            ext = witness
            G = GalGroup(ext)
            
        h1 = getattr(ext, 'is_galois', False)
        h2 = isinstance(G, GalGroup) and getattr(G, 'ext', None) == ext
        neg_q = not getattr(ext, 'is_finite', True)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a Galois extension",
    "H_2: G is the Galois group of L/K",
    r"¬Q: The map L \otimes_K L \to \prod_{\sigma \in G} L defined by x \otimes y \mapsto (x \sigma(y))_{\sigma \in G} is NOT an isomorphism of L-algebras"
]

N_HYP = 2
NEG_Q_INDEX = 2