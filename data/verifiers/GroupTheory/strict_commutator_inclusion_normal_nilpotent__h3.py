import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a nilpotent group
    try:
        h1_val = G.is_nilpotent() if callable(G.is_nilpotent) else G.is_nilpotent
        h1 = bool(h1_val)
    except Exception:
        h1 = False

    # H_2: H is a normal subgroup of G
    try:
        is_sub = True
        for gen in H.generators:
            if gen not in G:
                is_sub = False
                break
        
        is_norm = True
        if is_sub:
            for h in H.generators:
                for g in G.generators:
                    if (g * h * ~g) not in H:
                        is_norm = False
                        break
                if not is_norm:
                    break
        h2 = is_sub and is_norm
    except Exception:
        h2 = False

    # neg_Q: The commutator subgroup of H and G is NOT a proper subgroup of H
    try:
        try:
            H_elems = list(H.generate())
        except Exception:
            H_elems = list(H.elements)
            
        try:
            G_elems = list(G.generate())
        except Exception:
            G_elems = list(G.elements)
            
        comms = []
        for h in H_elems:
            for g in G_elems:
                comms.append(h * g * (~h) * (~g))
        
        CommHG = PermutationGroup(comms)
        
        is_sub_Comm = True
        for gen in CommHG.generators:
            if gen not in H:
                is_sub_Comm = False
                break
        
        CommHG_order = CommHG.order() if callable(CommHG.order) else CommHG.order
        H_order = H.order() if callable(H.order) else H.order
        
        is_proper = is_sub_Comm and (CommHG_order < H_order)
        
        neg_q = not is_proper
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: H is a normal subgroup of G",
    "¬Q: The commutator subgroup of H and G is not a proper subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2