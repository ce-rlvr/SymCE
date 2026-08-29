import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the hypotheses and falsifies the conclusion.
    In Field Theory, problems about subfields and splitting fields are standardly translated 
    to Galois theory:
      - L/K corresponds to a Galois group G.
      - Subfields E_1, E_2 correspond to subgroups H_1, H_2 <= G.
      - E_i is a splitting field over K iff H_i is a normal subgroup of G.
      - The intersection E_1 \cap E_2 corresponds to the join <H_1, H_2>.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, H1, H2 = witness
            elif len(witness) == 4:
                _, G, H1, H2 = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(H1, list):
            H1 = PermutationGroup(H1)
        if isinstance(H2, list):
            H2 = PermutationGroup(H2)
    except Exception:
        return [False, False, False]
        
    # H_1: Let L be an extension field of K
    # In the Galois correspondence, G = Gal(L/K), so L is always an extension of K.
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: Let E_1 and E_2 be subfields of L that are splitting fields over K
    # This translates to H_1 and H_2 being normal subgroups of G.
    try:
        def is_subgroup(grp, subgrp):
            for h in subgrp.generators:
                if h not in grp:
                    return False
            return True

        def is_normal(grp, subgrp):
            for g in grp.generators:
                for h in subgrp.generators:
                    # Conjugate of h by g must be in subgrp
                    if (g * h * ~g) not in subgrp:
                        return False
            return True

        h2_ok = (isinstance(H1, PermutationGroup) and isinstance(H2, PermutationGroup) and
                 is_subgroup(G, H1) and is_subgroup(G, H2) and
                 is_normal(G, H1) and is_normal(G, H2))
    except Exception:
        h2_ok = False
        
    # Conclusion: The intersection E_1 \cap E_2 is a splitting field over K
    # This translates to the join <H_1, H_2> being a normal subgroup of G.
    # We negate this to check if the conclusion FAILS.
    try:
        join_H = PermutationGroup(list(H1.generators) + list(H2.generators))
        neg_q = not is_normal(G, join_H)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: L is an extension field of K",
    "H_2: E_1 and E_2 are subfields of L that are splitting fields over K",
    "¬Q: The intersection E_1 \\cap E_2 is NOT a splitting field over K"
]

N_HYP = 2
NEG_Q_INDEX = 2