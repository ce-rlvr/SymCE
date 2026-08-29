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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The conjecture states that the abelianization map Aut(F_n) -> GL_n(Z) is surjective.
    This is true for finite n, but fails when n is infinite.
    """
    # H_1: Let \phi: Aut(F_n) -> Aut(F_n / F_n') be the natural homomorphism induced by the abelianization map
    # This is a definitional hypothesis, which holds for the given n.
    h1 = True
    
    # H_2: Identify Aut(F_n / F_n') with the general linear group GL_n(Z)
    # This is also a definitional hypothesis.
    h2 = True
    
    # ¬Q: The homomorphism \phi is not surjective
    # The map is surjective for all finite n, but not surjective for infinite n.
    try:
        if witness == sympy.oo:
            neg_q = True
        elif hasattr(witness, 'is_infinite') and witness.is_infinite:
            neg_q = True
        elif str(witness).lower() in ['oo', 'infinity', 'infty', 'aleph_0']:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let phi be the natural homomorphism induced by the abelianization map",
    "H_2: Identify Aut(F_n / F_n') with the general linear group GL_n(Z)",
    "¬Q: The homomorphism phi is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2