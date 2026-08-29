import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is nilpotent of class at most 2",
    "¬Q: Commutator bilinearity fails for some x, y, z in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: G is nilpotent of class at most 2
    try:
        if not h1_ok:
            h2_ok = False
        else:
            # Class at most 2 iff derived subgroup is contained in the center
            derived = witness.derived_subgroup()
            center = witness.center()
            h2_ok = derived.is_subgroup(center)
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion FAILS at the witness
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            elems = list(witness.elements)
            conclusion_holds = True
            
            for x in elems:
                for y in elems:
                    for z in elems:
                        # Commutator definition: comm(A, B) = A^-1 B^-1 A B
                        # In SymPy, this is ~A * ~B * A * B
                        
                        # Check comm(xy, z) == comm(x, z) * comm(y, z)
                        xy = x * y
                        comm_xy_z = ~xy * ~z * xy * z
                        comm_x_z = ~x * ~z * x * z
                        comm_y_z = ~y * ~z * y * z
                        if comm_xy_z != comm_x_z * comm_y_z:
                            conclusion_holds = False
                            break
                        
                        # Check comm(x, yz) == comm(x, y) * comm(x, z)
                        yz = y * z
                        comm_x_yz = ~x * ~yz * x * yz
                        comm_x_y = ~x * ~y * x * y
                        if comm_x_yz != comm_x_y * comm_x_z:
                            conclusion_holds = False
                            break
                    
                    if not conclusion_holds:
                        break
                if not conclusion_holds:
                    break
            
            neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]