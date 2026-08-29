import sympy
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import free_group

F, s, t = free_group("s, t")

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <s, t | R>",
    "¬Q: G is not isomorphic to the projective special linear group PSL(2, Z)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    try:
        if isinstance(witness, FpGroup) and len(witness.generators) == 2:
            h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if isinstance(witness, FpGroup):
            # PSL(2, Z) is the free product of Z2 and Z3, so its abelianization is Z6.
            # The invariant factors of its abelianization must be [6] (or [2, 3] depending on the SNF convention).
            # If the abelian invariants of G do not match this, G is definitely NOT isomorphic to PSL(2, Z).
            invs = witness.abelian_invariants()
            if sorted(invs) not in ([6], [2, 3]):
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]