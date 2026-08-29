import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]

    # H_1: N is a subgroup of G
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            h1_ok = False
        else:
            h1_ok = bool(N.is_subgroup(G))
    except Exception:
        h1_ok = False

    # ¬Q: N is not normal in G, or G/N is not cyclic
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            neg_q_ok = False
        elif not N.is_subgroup(G):
            # If N is not a subgroup, the conclusion trivially fails
            neg_q_ok = True
        elif not N.is_normal(G):
            # If N is not normal, the conclusion fails
            neg_q_ok = True
        else:
            # N is normal, check if G/N is cyclic
            order_quotient = G.order() // N.order()
            is_cyclic = False
            
            # G/N is cyclic iff there is an element g in G such that the order of gN in G/N is |G|/|N|
            for g in G.elements:
                m = 1
                curr = g
                while curr not in N and m <= order_quotient:
                    curr = curr * g
                    m += 1
                
                if m == order_quotient and curr in N:
                    is_cyclic = True
                    break
                    
            neg_q_ok = not is_cyclic
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a subgroup of G",
    "¬Q: N is not normal in G, or G/N is not cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1