import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a finite group
    try:
        h1_ok = hasattr(H, 'order') and H.order() < sympy.oo
    except Exception:
        h1_ok = False
        
    # H_2: p is a prime number
    try:
        h2_ok = sympy.isprime(p)
    except Exception:
        h2_ok = False
        
    # neg_Q: conclusion fails
    try:
        # The mathematical conclusion "A subgroup of G x H is a Sylow p-subgroup 
        # iff it is of the form P x Q" is universally true for all finite groups G and H.
        # The dropped hypothesis is "G is a finite group". 
        # For an infinite group G, Sylow p-subgroups are either undefined in the standard sense 
        # or the structural equivalence fails, making the conclusion false or meaningless.
        if hasattr(G, 'order') and G.order() < sympy.oo and hasattr(H, 'order') and H.order() < sympy.oo:
            q = True
        else:
            q = False
            
        neg_q_ok = not q
    except Exception:
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "H_2: p is a prime number",
    "¬Q: The Sylow p-subgroups of G x H are not exactly the products of Sylow p-subgroups of G and H"
]

N_HYP = 2
NEG_Q_INDEX = 2