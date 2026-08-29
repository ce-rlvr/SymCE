import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    witness is expected to be a tuple: (G, H, f, A, B)
    where:
      - G and H are groups (e.g., PermutationGroup)
      - f is a homomorphism from G to H (can be a dict or callable)
      - A and B are subgroups of G (can be PermutationGroup or iterable of elements)
    """
    try:
        G, H, f, A, B = witness
    except Exception:
        return [False, False, False, False]
        
    def apply_f(func, x):
        if isinstance(func, dict):
            return func[x]
        return func(x)

    G_elements = None
    H_elements = None

    # H_1: G and H are groups
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements')
        if h1:
            G_elements = list(G.elements)
            H_elements = set(H.elements)
    except Exception:
        h1 = False

    # H_2: f is a group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            for g in G_elements:
                val = apply_f(f, g)
                if val not in H_elements:
                    h2 = False
                    break
            if h2:
                for x in G_elements:
                    for y in G_elements:
                        if apply_f(f, x * y) != apply_f(f, x) * apply_f(f, y):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: A and B are subgroups of G
    try:
        if not h1:
            h3 = False
        else:
            def is_subgroup(S, G_set):
                if hasattr(S, 'elements'):
                    S_set = set(S.elements)
                else:
                    S_set = set(S)
                if not S_set or not S_set.issubset(G_set):
                    return False, set()
                for x in S_set:
                    for y in S_set:
                        if x * y not in S_set:
                            return False, set()
                return True, S_set

            G_elements_set = set(G_elements)
            A_is_sub, A_elements = is_subgroup(A, G_elements_set)
            B_is_sub, B_elements = is_subgroup(B, G_elements_set)
            h3 = A_is_sub and B_is_sub
    except Exception:
        h3 = False

    # ¬Q: f(A ∩ B) ≠ f(A) ∩ f(B)
    try:
        if hasattr(A, 'elements'):
            A_set = set(A.elements)
        else:
            A_set = set(A)
            
        if hasattr(B, 'elements'):
            B_set = set(B.elements)
        else:
            B_set = set(B)
            
        A_cap_B = A_set.intersection(B_set)
        
        f_A = {apply_f(f, x) for x in A_set}
        f_B = {apply_f(f, x) for x in B_set}
        f_A_cap_B = {apply_f(f, x) for x in A_cap_B}
        
        f_A_cap_f_B = f_A.intersection(f_B)
        
        neg_q = f_A_cap_B != f_A_cap_f_B
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a group homomorphism from G to H",
    "H_3: A and B are subgroups of G",
    "¬Q: f(A ∩ B) ≠ f(A) ∩ f(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3