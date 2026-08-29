import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_image(p, i):
    """Safely get the image of i under permutation p, handling size differences."""
    if i < p.size:
        return p.array_form[i]
    return i

def group_contains(group_elements, p):
    """Check if permutation p is in group_elements, robust to degree/size differences."""
    for q in group_elements:
        size = max(p.size, q.size)
        match = True
        for i in range(size):
            if get_image(p, i) != get_image(q, i):
                match = False
                break
        if match:
            return True
    return False

def conditions(witness):
    try:
        G, S = witness
    except Exception:
        return [False, False]
    
    h1 = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(S, PermutationGroup):
            G_elements = list(G.generate())
            # Verify S is a subgroup of G
            is_subgroup = all(group_contains(G_elements, s) for s in S.generators)
            
            if is_subgroup:
                # Check if G is semisimple (has no non-trivial solvable normal subgroups)
                # Equivalently, the normal closure of any non-identity element is not solvable.
                is_semi = True
                for g in G_elements:
                    is_id = True
                    for i in range(g.size):
                        if get_image(g, i) != i:
                            is_id = False
                            break
                    if is_id:
                        continue
                    
                    class_g = set()
                    for h in G_elements:
                        conj = h * g * ~h
                        class_g.add(conj)
                    
                    N = PermutationGroup(list(class_g))
                    if N.is_solvable:
                        is_semi = False
                        break
                h1 = is_semi
    except Exception:
        h1 = False

    neg_q = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(S, PermutationGroup):
            G_elements = list(G.generate())
            is_subgroup = all(group_contains(G_elements, s) for s in S.generators)
            
            if is_subgroup:
                S_elements = list(S.generate())
                # The normalizer of S in G is NOT a proper subgroup of G iff N_G(S) == G.
                # This means S is a normal subgroup of G.
                is_normal = True
                for g in G_elements:
                    for s in S.generators:
                        conj = g * s * ~g
                        if not group_contains(S_elements, conj):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = is_normal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "¬Q: The normalizer of S in G is not a proper subgroup of G (i.e. S is normal in G)"
]

N_HYP = 1
NEG_Q_INDEX = 1