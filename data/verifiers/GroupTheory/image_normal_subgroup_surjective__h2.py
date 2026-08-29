import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Standard group theory objects for witness construction
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, H, f, N)
    where G and H are PermutationGroups, f is a dict or callable mapping G to H,
    and N is a normal subgroup of G (as a PermutationGroup or list of elements).
    """
    try:
        G, H, f, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # Setup f_func for subsequent checks
    try:
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        elif callable(f):
            f_func = f
        else:
            f_func = None
    except Exception:
        f_func = None

    # H_2: f is surjective
    try:
        if not h1 or f_func is None:
            h2 = False
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            image = set()
            h2_ok = True
            for g in G_elements:
                val = f_func(g)
                if val not in H_elements:
                    h2_ok = False
                    break
                image.add(val)
            if h2_ok:
                h2 = image == set(H_elements)
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        if not h1:
            h3 = False
        else:
            if isinstance(N, PermutationGroup):
                N_elements = list(N.elements)
            else:
                N_elements = list(N)
                
            N_set = set(N_elements)
            G_elements_set = set(G.elements)
            
            if not N_set.issubset(G_elements_set):
                h3 = False
            elif G.identity not in N_set:
                h3 = False
            else:
                is_subgroup = True
                for n1 in N_set:
                    if ~n1 not in N_set:
                        is_subgroup = False
                        break
                    for n2 in N_set:
                        if n1 * n2 not in N_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                if not is_subgroup:
                    h3 = False
                else:
                    is_normal = True
                    for g in G_elements_set:
                        for n in N_set:
                            if g * n * ~g not in N_set:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                    h3 = is_normal
    except Exception:
        h3 = False

    # ¬Q: f(N) is not a normal subgroup of H
    try:
        if not h1 or f_func is None:
            neg_q = False
        else:
            if isinstance(N, PermutationGroup):
                N_elements = list(N.elements)
            else:
                N_elements = list(N)
            N_set = set(N_elements)
            
            f_N = set(f_func(n) for n in N_set)
            
            is_subgroup = True
            if H.identity not in f_N:
                is_subgroup = False
            else:
                for y1 in f_N:
                    if ~y1 not in f_N:
                        is_subgroup = False
                        break
                    for y2 in f_N:
                        if y1 * y2 not in f_N:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
            if not is_subgroup:
                # If it's not even a subgroup, it's not a normal subgroup.
                neg_q = True
            else:
                # It is a subgroup, check if it is normal
                is_normal = True
                for h in H.elements:
                    for y in f_N:
                        if h * y * ~h not in f_N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is surjective",
    "H_3: N is a normal subgroup of G",
    "¬Q: f(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3