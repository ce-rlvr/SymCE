import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]

    # Extract elements of G
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            G_elems = set(G.generate_dimino())
        else:
            G_elems = set()
    except Exception:
        h1 = False
        G_elems = set()

    # Extract elements of N
    try:
        if hasattr(N, 'generate_dimino'):
            N_elems = set(N.generate_dimino())
        elif hasattr(N, 'elements'):
            N_elems = set(N.elements)
        else:
            N_elems = set(N)
    except Exception:
        N_elems = set()

    # Extract elements of H
    try:
        if hasattr(H, 'generate_dimino'):
            H_elems = set(H.generate_dimino())
        elif hasattr(H, 'elements'):
            H_elems = set(H.elements)
        else:
            H_elems = set(H)
    except Exception:
        H_elems = set()

    # Identify the identity element of G
    try:
        if G_elems:
            id_G = list(G_elems)[0] ** 0
        else:
            id_G = None
    except Exception:
        id_G = None

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if h1 and N_elems and id_G is not None:
            if N_elems.issubset(G_elems):
                # Check if N is a valid subgroup
                is_N_group = True
                if id_G not in N_elems:
                    is_N_group = False
                else:
                    for a in N_elems:
                        if ~a not in N_elems:
                            is_N_group = False
                            break
                        for b in N_elems:
                            if a * b not in N_elems:
                                is_N_group = False
                                break
                
                # Check if N is normal in G
                if is_N_group:
                    h2 = True
                    for g in G_elems:
                        for n in N_elems:
                            if (~g * n * g) not in N_elems:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H_3: G = NH
    try:
        h3 = False
        if h1 and h2 and H_elems:
            NH_elems = {n * h for n in N_elems for h in H_elems}
            h3 = (G_elems == NH_elems)
    except Exception:
        h3 = False

    # H_4: N \cap H = {e}
    try:
        h4 = False
        if h1 and h2 and H_elems and id_G is not None:
            h4 = (N_elems.intersection(H_elems) == {id_G})
    except Exception:
        h4 = False

    # ¬Q: G/N is not isomorphic to H
    # (Since H is a subset of G, if it is not a subgroup, it is not a group, 
    # hence it cannot be isomorphic to the quotient group G/N)
    try:
        neg_q = False
        if h1 and H_elems and id_G is not None:
            is_group = True
            if id_G not in H_elems:
                is_group = False
            else:
                for a in H_elems:
                    if ~a not in H_elems:
                        is_group = False
                        break
                    for b in H_elems:
                        if a * b not in H_elems:
                            is_group = False
                            break
            neg_q = not is_group
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: G = NH",
    "H_4: N \\cap H = \\{e\\}",
    "¬Q: G/N is not isomorphic to H"
]

N_HYP = 4
NEG_Q_INDEX = 4