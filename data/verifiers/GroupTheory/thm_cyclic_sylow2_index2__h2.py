import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The Sylow 2-subgroup of G is cyclic
    try:
        if not h1:
            h2 = False
        else:
            order = witness.order()
            k = 0
            temp = order
            while temp % 2 == 0:
                temp //= 2
                k += 1
            target = 2**k
            
            if target == 1:
                h2 = True
            else:
                # If the Sylow 2-subgroup has order 2^k, it is cyclic iff 
                # there is an element of order 2^k in the Sylow 2-subgroup.
                # By Sylow theorems, all Sylow 2-subgroups are conjugate, 
                # so it's cyclic iff G contains an element of order 2^k.
                h2 = False
                if order <= 5000:
                    for g in witness.elements:
                        if g.order() == target:
                            h2 = True
                            break
                else:
                    # Fallback for larger groups if sylow_subgroup is available
                    s2 = witness.sylow_subgroup(2)
                    h2 = s2.is_cyclic
    except Exception:
        h2 = False

    # neg_Q: G does not possess a normal subgroup of index 2
    try:
        if not h1:
            neg_q = False
        else:
            # G has a normal subgroup of index 2 iff its abelianization has even order.
            # Abelianization order = |G| / |G'|
            derived_order = witness.derived_subgroup().order()
            ab_order = witness.order() // derived_order
            has_index_2 = (ab_order % 2 == 0)
            neg_q = not has_index_2
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The Sylow 2-subgroup of G is cyclic",
    "¬Q: G does not possess a normal subgroup of index 2"
]

N_HYP = 2
NEG_Q_INDEX = 2