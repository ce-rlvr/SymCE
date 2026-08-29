import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Standard group theory objects for potential witnesses
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If G1, G2 are groups and N2 is a normal subgroup of G2, 
    then (G1 x G2) / (N1 x N2) is isomorphic to (G1 / N1) x (G2 / N2)."
    
    The dropped hypothesis is that N1 must be a normal subgroup of G1.
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    def pad_group(H, degree):
        """Pads a permutation group to a larger degree by adding fixed points."""
        if H.degree == degree:
            return H
        if H.degree > degree:
            raise ValueError("Subgroup degree larger than parent group degree")
        new_gens = []
        for g in H.generators:
            arr = g.array_form
            arr = arr + list(range(len(arr), degree))
            new_gens.append(Permutation(arr))
        if not new_gens:
            new_gens.append(Permutation(list(range(degree))))
        return PermutationGroup(new_gens)

    # H_1: G1 and G2 are groups, and N1, N2 are subgroups of G1, G2 respectively
    try:
        h1 = (isinstance(G1, PermutationGroup) and 
              isinstance(G2, PermutationGroup) and 
              isinstance(N1, PermutationGroup) and 
              isinstance(N2, PermutationGroup) and 
              N1.is_subgroup(G1) and 
              N2.is_subgroup(G2))
    except Exception:
        h1 = False

    # H_2: N2 is a normal subgroup of G2
    try:
        h2 = bool(N2.is_normal(G2))
    except Exception:
        h2 = False

    # neg_Q: The quotient group (G1 × G2) / (N1 × N2) is NOT isomorphic to (G1 / N1) × (G2 / N2)
    try:
        if not h1:
            neg_q = True
        elif not N1.is_normal(G1):
            # If N1 is not normal in G1, G1/N1 is not a valid group, so they cannot be isomorphic.
            neg_q = True
        else:
            N1_p = pad_group(N1, G1.degree)
            N2_p = pad_group(N2, G2.degree)
            
            prod_G = G1 * G2
            prod_N = N1_p * N2_p
            
            if not prod_N.is_normal(prod_G):
                neg_q = True
            else:
                Q_prod = prod_G.quotient_group(prod_N)
                Q1 = G1.quotient_group(N1)
                Q2 = G2.quotient_group(N2)
                Q_sep = Q1 * Q2
                neg_q = not bool(Q_prod.is_isomorphic(Q_sep))
    except Exception:
        # If any group operation fails (e.g., invalid quotient), the conclusion fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G1 and G2 are groups, and N1, N2 are subgroups of G1, G2 respectively",
    "H_2: N2 is a normal subgroup of G2",
    "¬Q: The quotient group (G1 × G2) / (N1 × N2) is NOT isomorphic to (G1 / N1) × (G2 / N2)"
]

N_HYP = 2
NEG_Q_INDEX = 2