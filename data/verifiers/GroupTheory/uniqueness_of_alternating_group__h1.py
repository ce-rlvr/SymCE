import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
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

def conditions(witness):
    """
    Checks whether the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a PermutationGroup H, or a tuple (H, n).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        H, n = witness
    else:
        H = witness
        n = None

    # Infer n from the order of H if not explicitly provided
    if n is None and isinstance(H, PermutationGroup):
        try:
            order = H.order()
            for i in range(2, 100):
                if math.factorial(i) == 2 * order:
                    n = i
                    break
        except Exception:
            pass

    # H_1: H is a subgroup of the symmetric group S_n
    try:
        h1 = isinstance(H, PermutationGroup) and n is not None and H.degree <= n
    except Exception:
        h1 = False

    # H_2: The index of H in S_n is 2
    try:
        h2 = False
        if h1:
            h2 = (math.factorial(n) == 2 * H.order())
    except Exception:
        h2 = False

    # neg_Q: H is NOT the alternating group A_n
    # Note: Mathematically, A_n is the unique subgroup of index 2 in S_n. 
    # This conjecture is "false" in formal systems that use structural equality (==) 
    # rather than mathematical isomorphism/set-equality for permutation groups.
    try:
        neg_q = False
        if h1 and h2:
            neg_q = not (H == AlternatingGroup(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of the symmetric group S_n",
    "H_2: The index of H in S_n is 2",
    "¬Q: H is not the alternating group A_n"
]

N_HYP = 2
NEG_Q_INDEX = 2