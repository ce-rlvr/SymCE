import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    # H_1: H is a subgroup of G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
            
        h1_ok = True
        if not hasattr(H, 'generators') or not hasattr(G, 'contains'):
            h1_ok = False
        else:
            for gen in H.generators:
                if G.contains(gen):
                    continue
                
                # Attempt to handle degree mismatches between H and G
                try:
                    if gen.size < G.degree:
                        padded = Permutation(gen.array_form + list(range(gen.size, G.degree)))
                        if G.contains(padded):
                            continue
                    elif gen.size > G.degree:
                        if all(gen(i) == i for i in range(G.degree, gen.size)):
                            truncated = Permutation(gen.array_form[:G.degree])
                            if G.contains(truncated):
                                continue
                except Exception:
                    pass
                
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # ¬Q: H is not a cyclic group
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, H = witness
        else:
            H = witness
            
        order = H.order()
        if order > 10000:
            # Prevent timeout for excessively large groups
            neg_q_ok = False
        else:
            is_cyc = False
            for g in H.elements:
                if g.order() == order:
                    is_cyc = True
                    break
            neg_q_ok = not is_cyc
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1