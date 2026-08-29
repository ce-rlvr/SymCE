import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
trivial = PermutationGroup([Permutation(0)])

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (G, H) representing the Galois group G of L/K
    and the subgroup H corresponding to the intermediate field E (i.e., H = Gal(L/E)).
    """
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: L/K is a finite Galois extension with Galois group G
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: E is an intermediate field between K and L
    # This corresponds to H being a subgroup of G.
    try:
        if isinstance(H, PermutationGroup):
            h_gens = []
            for h in H.generators:
                arr = h.array_form
                if len(arr) < G.degree:
                    arr = arr + list(range(len(arr), G.degree))
                elif len(arr) > G.degree:
                    if arr[G.degree:] != list(range(G.degree, len(arr))):
                        raise ValueError("H moves points outside G's domain")
                    arr = arr[:G.degree]
                h_gens.append(Permutation(arr))
            H_resized = PermutationGroup(h_gens)
            h2 = all(g in G for g in H_resized.generators)
            H = H_resized  # Use the resized H for the normality check
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The restriction map is NOT a well-defined surjective homomorphism with kernel Gal(L/E)
    # This happens if and only if E/K is not a normal extension, which corresponds to H not being a normal subgroup of G.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            is_normal = True
            for g in G.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        is_normal = False
                        break
                    if (~g * h * g) not in H:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension with Galois group G",
    "H_2: E is an intermediate field between K and L",
    "¬Q: The restriction map is not a well-defined surjective homomorphism with kernel Gal(L/E)"
]

N_HYP = 2
NEG_Q_INDEX = 2