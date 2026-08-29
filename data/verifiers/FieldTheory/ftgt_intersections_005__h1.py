import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(H, G):
    """Check if H is a subgroup of G."""
    try:
        for g in H.generators:
            if not G.contains(g):
                return False
        return True
    except Exception:
        return False

def normalizer(V, U):
    """Compute the normalizer of U in V."""
    try:
        if V.order() > 2000:
            return None
        gens = []
        for g in V.generate():
            is_norm = True
            for u in U.generators:
                # Check if g * u * g^-1 is in U
                # In SymPy, permutations are applied left-to-right, so conjugate is ~g * u * g
                if not U.contains(~g * u * g):
                    is_norm = False
                    break
            if is_norm:
                gens.append(g)
        if not gens:
            gens = [V.identity]
        return PermutationGroup(gens)
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    """
    The witness is expected to be a tuple (G, U, V1, V2) of PermutationGroup objects.
    This represents the Galois correspondence where:
    - G is the Galois group of the Galois closure L/F.
    - U is the subgroup fixing K.
    - V1 is the subgroup fixing E1.
    - V2 is the subgroup fixing E2.
    """
    try:
        if len(witness) == 4:
            G, U, V1, V2 = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: E_1 and E_2 are intermediate fields between F and K
    # In the Galois correspondence, this means U <= V1 <= G and U <= V2 <= G
    try:
        h1_ok = bool(is_subgroup(U, V1) and is_subgroup(V1, G) and 
                     is_subgroup(U, V2) and is_subgroup(V2, G))
    except Exception:
        h1_ok = False

    # H_2: H_1 = Gal(K/E_1) and H_2 = Gal(K/E_2) are the corresponding subgroups of G
    # This is true by definition in our group-theoretic translation, provided the witness
    # consists of valid PermutationGroup objects.
    try:
        h2_ok = bool(isinstance(G, PermutationGroup) and isinstance(U, PermutationGroup) and
                     isinstance(V1, PermutationGroup) and isinstance(V2, PermutationGroup))
    except Exception:
        h2_ok = False

    # neg_Q: The subgroup corresponding to E_1 \cap E_2 is NOT \langle H_1, H_2 \rangle
    # E_1 \cap E_2 corresponds to W = \langle V1, V2 \rangle
    # Gal(K / (E_1 \cap E_2)) corresponds to N_W(U)
    # \langle H_1, H_2 \rangle corresponds to \langle N_{V1}(U), N_{V2}(U) \rangle
    try:
        W_gens = list(V1.generators) + list(V2.generators)
        W = PermutationGroup(W_gens)
        
        N_W_U = normalizer(W, U)
        N_V1_U = normalizer(V1, U)
        N_V2_U = normalizer(V2, U)
        
        if N_W_U is None or N_V1_U is None or N_V2_U is None:
            neg_q = False
        else:
            H1_H2_gens = list(N_V1_U.generators) + list(N_V2_U.generators)
            H1_H2_gen_group = PermutationGroup(H1_H2_gens)
            
            # Check if N_W_U == H1_H2_gen_group
            eq = is_subgroup(N_W_U, H1_H2_gen_group) and is_subgroup(H1_H2_gen_group, N_W_U)
            neg_q = not eq
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: E_1 and E_2 are intermediate fields between F and K",
    "H_2: H_1 = Gal(K/E_1) and H_2 = Gal(K/E_2) are the corresponding subgroups of G",
    "¬Q: The subgroup corresponding to E_1 \\cap E_2 is NOT \\langle H_1, H_2 \\rangle"
]

N_HYP = 2
NEG_Q_INDEX = 2