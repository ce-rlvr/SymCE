import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            x = witness['x']
            y = witness['y']
            phi = witness['phi']
        else:
            G, H, x, y, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x and y are elements of G
    try:
        h2 = x in G and y in G
    except Exception:
        h2 = False

    # neg_Q: phi(commutator(x, y)) != commutator(phi(x), phi(y))
    try:
        comm_xy_1 = x**-1 * y**-1 * x * y
        comm_xy_2 = x * y * x**-1 * y**-1
        
        if callable(phi):
            phi_x = phi(x)
            phi_y = phi(y)
            
            try:
                phi_comm_1 = phi(comm_xy_1)
                comm_phix_phiy_1 = phi_x**-1 * phi_y**-1 * phi_x * phi_y
                neg_q_1 = (phi_comm_1 != comm_phix_phiy_1) and (phi_comm_1 in H)
            except Exception:
                neg_q_1 = False
                
            try:
                phi_comm_2 = phi(comm_xy_2)
                comm_phix_phiy_2 = phi_x * phi_y * phi_x**-1 * phi_y**-1
                neg_q_2 = (phi_comm_2 != comm_phix_phiy_2) and (phi_comm_2 in H)
            except Exception:
                neg_q_2 = False
                
        else:
            phi_x = phi[x]
            phi_y = phi[y]
            
            if comm_xy_1 in phi:
                phi_comm_1 = phi[comm_xy_1]
                comm_phix_phiy_1 = phi_x**-1 * phi_y**-1 * phi_x * phi_y
                neg_q_1 = (phi_comm_1 != comm_phix_phiy_1) and (phi_comm_1 in H)
            else:
                neg_q_1 = False
                
            if comm_xy_2 in phi:
                phi_comm_2 = phi[comm_xy_2]
                comm_phix_phiy_2 = phi_x * phi_y * phi_x**-1 * phi_y**-1
                neg_q_2 = (phi_comm_2 != comm_phix_phiy_2) and (phi_comm_2 in H)
            else:
                neg_q_2 = False

        neg_q = bool(neg_q_1 or neg_q_2)
        
        if phi_x not in H or phi_y not in H:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G and H are groups", "H_2: x and y are elements of G", "not Q: phi(commutator(x, y)) != commutator(phi(x), phi(y))"]
N_HYP = 2
NEG_Q_INDEX = 2