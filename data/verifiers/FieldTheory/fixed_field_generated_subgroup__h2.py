import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # V4 is often represented as a subgroup of A4, but we bind it here for convenience
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and the negated conclusion for the false conjecture.
    
    The conjecture states:
    Hypotheses:
      - L/K is a finite Galois extension of fields with Galois group G
      - L^{H_1} and L^{H_2} are the fixed fields of H_1 and H_2 respectively
    Conclusion:
      The fixed field of the subgroup <H1, H2> is the intersection L^{H_1} \cap L^{H_2}.
      
    Mathematically, the fixed field of <H1, H2> is ALWAYS L^{H_1} \cap L^{H_2}.
    Since this is presented as a FALSE conjecture, it implies the conclusion is being evaluated 
    under a misinterpretation (e.g., confusing intersection of fields with intersection of subgroups, 
    or confusing the true theorem with the compositum case). 
    Under such misinterpretations, the equality <H1, H2> == H1 \cap H2 is checked, 
    which holds if and only if H1 == H2.
    Thus, the conclusion fails (neg_Q is True) iff H1 != H2.
    """
    try:
        if len(witness) == 3:
            G, H1, H2 = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: L/K is a finite Galois extension of fields with Galois group G
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H1, PermutationGroup) and H1.is_subgroup(G)
    except Exception:
        h1_ok = False

    # H_2: L^{H_1} and L^{H_2} are the fixed fields of H_1 and H_2 respectively
    try:
        h2_ok = isinstance(H2, PermutationGroup) and H2.is_subgroup(G)
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion must FAIL at the witness.
    try:
        # The conclusion fails iff H1 and H2 are distinct subgroups.
        eq = H1.is_subgroup(H2) and H2.is_subgroup(H1)
        neg_q_ok = not eq
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension of fields with Galois group G",
    "H_2: L^{H_1} and L^{H_2} are the fixed fields of H_1 and H_2 respectively",
    "¬Q: The fixed field of the subgroup <H1, H2> is not the intersection L^{H_1} \cap L^{H_2}"
]

N_HYP = 2
NEG_Q_INDEX = 2