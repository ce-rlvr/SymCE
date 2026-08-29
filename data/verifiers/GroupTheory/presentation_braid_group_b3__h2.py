import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: Let G be a group defined by the presentation <σ_1, σ_2 | R>.
    h1_ok = False
    try:
        if hasattr(witness, 'generators'):
            h1_ok = len(witness.generators) == 2
    except Exception:
        pass

    # ¬Q: The group G is NOT isomorphic to the braid group on 3 strands, B_3.
    neg_q_ok = False
    try:
        if isinstance(witness, PermutationGroup):
            # B_3 is infinite; any permutation group in SymPy is finite.
            neg_q_ok = True
        elif type(witness).__name__ == 'FreeGroup':
            # B_3 is not a free group.
            neg_q_ok = True
        elif type(witness).__name__ == 'FpGroup':
            # B_3 has abelianization isomorphic to Z, so its abelian invariants must be [0].
            invs = witness.abelian_invariants()
            if invs != [0]:
                neg_q_ok = True
            else:
                # If abelian invariants are [0], check if the group is abelian.
                # B_3 is non-abelian. If the generators commute, it's not B_3.
                gens = witness.generators
                if len(gens) == 2:
                    g1, g2 = gens
                    comm = g1 * g2 * g1**-1 * g2**-1
                    if comm == witness.identity:
                        neg_q_ok = True
        else:
            # Fallback for other types of groups
            if hasattr(witness, 'order'):
                if witness.order() != sympy.oo:
                    neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group defined by a presentation with 2 generators",
    "¬Q: G is not isomorphic to B_3"
]

N_HYP = 1
NEG_Q_INDEX = 1