import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: The map phi(x) = x^(-1) is NOT a group isomorphism from G to G^op
    try:
        if not h1:
            neg_q = False
        else:
            is_iso = True
            elements = list(witness.generate())
            
            # Check homomorphism property: phi(x * y) == phi(x) *_{op} phi(y)
            # In G^op, the operation is defined as a *_{op} b = b * a
            for x in elements:
                for y in elements:
                    xy = x * y
                    phi_xy = xy**(-1)
                    
                    phi_x = x**(-1)
                    phi_y = y**(-1)
                    op_phi_x_phi_y = phi_y * phi_x  # G^op operation
                    
                    if phi_xy != op_phi_x_phi_y:
                        is_iso = False
                        break
                if not is_iso:
                    break
            
            # Check bijection property
            if is_iso:
                mapped = set(x**(-1) for x in elements)
                if len(mapped) != len(elements):
                    is_iso = False
                    
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The map phi(x) = x^(-1) is not a group isomorphism from G to G^op"
]

N_HYP = 1
NEG_Q_INDEX = 1