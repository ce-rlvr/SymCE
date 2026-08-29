import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            G = witness[0]
            H = witness[1]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: index of H in G is n for some integer n > 0
    try:
        if h1 and h2:
            n = G.order() // H.order()
            h3 = (G.order() % H.order() == 0) and (n > 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            elements_G = list(G.elements)
            core_elements = []
            for x in list(H.elements):
                is_in_core = True
                for g in elements_G:
                    conj = (~g) * x * g
                    if conj not in H:
                        is_in_core = False
                        break
                if is_in_core:
                    core_elements.append(x)
            
            if not core_elements:
                core_elements = [G.identity]
            core = PermutationGroup(core_elements)

            kernel = None
            if len(witness) >= 3:
                K = witness[2]
                if isinstance(K, PermutationGroup):
                    kernel = K
                elif hasattr(K, 'kernel'):
                    kernel = K.kernel() if callable(K.kernel) else K.kernel
                elif isinstance(K, list) and len(K) > 0 and isinstance(K[0], Permutation):
                    kernel = PermutationGroup(K)

            if kernel is not None:
                kernel_is_core = kernel.is_subgroup(core) and core.is_subgroup(kernel)
                neg_q = not kernel_is_core
            else:
                # If no kernel is provided, assume the natural action of G
                # The kernel of the natural action of a PermutationGroup is trivial
                trivial_group = PermutationGroup([G.identity])
                kernel_is_core = trivial_group.is_subgroup(core) and core.is_subgroup(trivial_group)
                neg_q = not kernel_is_core
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: index of H in G is n for some integer n > 0",
    "¬Q: The conclusion fails"
]

N_HYP = 3
NEG_Q_INDEX = 3