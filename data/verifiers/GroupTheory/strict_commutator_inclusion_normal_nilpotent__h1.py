from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup

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
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(H.is_subgroup(G) and H.is_normal(G))
    except Exception:
        h1 = False

    try:
        h2 = bool(H.order() > 1)
    except Exception:
        h2 = False

    try:
        gens = []
        for g in list(G.generate()):
            for h in list(H.generate()):
                gens.append((g**-1) * (h**-1) * g * h)
        
        C = PermutationGroup(gens)
        is_proper = C.is_subgroup(H) and C.order() < H.order()
        neg_q = not is_proper
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a normal subgroup of G",
    "H_2: H is not the trivial subgroup",
    "not Q: The commutator subgroup of H and G is not a proper subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2