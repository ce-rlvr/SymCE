import sympy
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    H1 = False
    neg_Q = False
    
    try:
        if isinstance(witness, PermutationGroup) and witness.order() > 1:
            # Definition 1: Direct product of simple groups (completely reducible group)
            normal_subs = witness.normal_subgroups()
            min_normals = []
            for N in normal_subs:
                if N.order() > 1:
                    is_minimal = True
                    for M in normal_subs:
                        if 1 < M.order() < N.order() and all(g in N for g in M.generators):
                            is_minimal = False
                            break
                    if is_minimal:
                        min_normals.append(N)
            
            gens = []
            for N in min_normals:
                gens.extend(N.generators)
            
            if gens:
                gen_group = PermutationGroup(gens)
                if gen_group.order() == witness.order():
                    H1 = True

            # Definition 2: Central product of quasisimple groups (finite analogue of semisimple Lie groups)
            if not H1 and witness.derived_subgroup().order() == witness.order():
                Z = witness.center()
                N_containing_Z = []
                for N in normal_subs:
                    if N.order() > Z.order():
                        if all(g in N for g in Z.generators):
                            N_containing_Z.append(N)
                
                min_normals_Z = []
                for N in N_containing_Z:
                    is_minimal = True
                    for M in N_containing_Z:
                        if M.order() < N.order() and all(g in N for g in M.generators):
                            is_minimal = False
                            break
                    if is_minimal:
                        min_normals_Z.append(N)
                
                if min_normals_Z:
                    gens_Z = []
                    for N in min_normals_Z:
                        gens_Z.extend(N.generators)
                    gen_group_Z = PermutationGroup(gens_Z)
                    if gen_group_Z.order() == witness.order():
                        H1 = True
    except Exception:
        H1 = False

    try:
        if isinstance(witness, PermutationGroup):
            # The natural homomorphism G -> Aut(G) has kernel Z(G).
            # It is injective iff Z(G) is trivial.
            # Inn(G) is isomorphic to G/Z(G), so G is isomorphic to Inn(G) iff Z(G) is trivial (for finite groups).
            # The conclusion fails (neg_Q is True) iff Z(G) is non-trivial.
            neg_Q = witness.center().order() > 1
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "¬Q: The natural homomorphism G -> Aut(G) is not injective, or G is not isomorphic to Inn(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1