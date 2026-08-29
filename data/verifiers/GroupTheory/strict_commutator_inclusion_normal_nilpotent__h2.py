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

def get_order(grp):
    return grp.order() if callable(grp.order) else grp.order

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        is_nilp = G.is_nilpotent() if callable(G.is_nilpotent) else G.is_nilpotent
        h_in_g = all(g in G for g in H.generators)
        h1_ok = bool(is_nilp and h_in_g)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(get_order(H) > 1)
    except Exception:
        h2_ok = False

    try:
        if get_order(G) > 100:
            neg_q_ok = False
        else:
            gens = []
            for h in list(H.elements):
                for g in list(G.elements):
                    gens.append((h**-1) * (g**-1) * h * g)
            
            if not gens:
                comm = trivial
            else:
                comm = PermutationGroup(gens)
            
            is_subgroup = all(c in H for c in comm.generators)
            is_proper = is_subgroup and (get_order(comm) < get_order(H))
            
            neg_q_ok = not is_proper
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group and H is a subgroup of G",
    "H_2: H is not the trivial subgroup",
    "not Q: The commutator subgroup of H and G is not a proper subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2