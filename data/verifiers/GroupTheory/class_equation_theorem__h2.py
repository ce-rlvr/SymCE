import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        G, R_iterable = witness
        R = list(R_iterable)
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: R is a set of representatives for the distinct conjugacy classes of G that are not contained in Z(G)
    try:
        elements = list(G.elements)
        classes = []
        for x in elements:
            c_x = {g * x * ~g for g in elements}
            if c_x not in classes:
                classes.append(c_x)
        non_central_classes = [c for c in classes if len(c) > 1]
        
        R_set = set(R)
        if len(R_set) != len(R):
            h2_ok = False
        elif len(R_set) != len(non_central_classes):
            h2_ok = False
        else:
            h2_ok = True
            for c in non_central_classes:
                if len(R_set.intersection(c)) != 1:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False
        
    # ¬Q: The order of G is not equal to the order of Z(G) plus the sum over all x in R of the index of C_G(x) in G
    try:
        elements = list(G.elements)
        Z_G = {x for x in elements if all(g * x == x * g for g in elements)}
        order_Z = len(Z_G)
        
        sum_indices = 0
        for x in R:
            C_G_x = {g for g in elements if g * x == x * g}
            index = len(elements) // len(C_G_x)
            sum_indices += index
            
        neg_q_ok = bool(len(elements) != order_Z + sum_indices)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: R is a set of representatives for the distinct conjugacy classes of G that are not contained in Z(G)",
    "¬Q: The order of G is not equal to the order of Z(G) plus the sum over all x in R of the index of C_G(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2