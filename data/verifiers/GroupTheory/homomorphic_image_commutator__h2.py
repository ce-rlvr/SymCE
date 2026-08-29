import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
        else:
            G, H, phi = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        def apply_phi(g):
            if isinstance(phi, dict):
                return phi[g]
            elif callable(phi):
                return phi(g)
            else:
                for k, v in phi:
                    if k == g:
                        return v
                raise ValueError("Mapping not found")

        # Evaluate the commutator subgroup of G and its image under phi
        G_prime = G.derived_subgroup()
        phi_G_prime = set(apply_phi(g) for g in G_prime.elements)

        # Evaluate the image of G under phi and the commutator subgroup of the group it generates
        phi_G_elements = list(set(apply_phi(g) for g in G.elements))
        phi_G_group = PermutationGroup(*phi_G_elements)
        
        phi_G_prime_group = phi_G_group.derived_subgroup()
        phi_G_prime_group_elements = set(phi_G_prime_group.elements)

        # The conclusion fails if the image of G' is not equal to the commutator subgroup of the image of G
        neg_q = phi_G_prime != phi_G_prime_group_elements
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: ϕ(G') != (ϕ(G))'"
]

N_HYP = 1
NEG_Q_INDEX = 1