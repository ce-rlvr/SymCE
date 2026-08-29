import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: G is a group (and M, N are subgroups)",
    "H_2: N is a normal subgroup of G",
    "H_3: G = MN",
    "¬Q: G/(M \\cap N) is not isomorphic to (G/M) \\times (G/N)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            M = witness.get('M')
            N = witness.get('N')
        else:
            G, M, N = witness
    except Exception:
        return [False, False, False, False]
    
    def is_subgroup(H, Grp):
        try:
            if hasattr(H, 'is_subgroup'):
                return H.is_subgroup(Grp)
            return all(g in Grp for g in H.generators)
        except Exception:
            return False

    def is_normal(H, Grp):
        try:
            if hasattr(H, 'is_normal'):
                return H.is_normal(Grp)
            for g in Grp.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        return False
                    if (~g * h * g) not in H:
                        return False
            return True
        except Exception:
            return False

    def intersect_order(H1, H2):
        count = 0
        try:
            elements = H1.elements
        except AttributeError:
            elements = list(H1.generate_dimino())
        for g in elements:
            if g in H2:
                count += 1
        return count

    def get_order(Grp):
        if callable(Grp.order):
            return Grp.order()
        return Grp.order

    # H1: G is a group, M is a subgroup, N is a subgroup
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(M, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              is_subgroup(M, G) and 
              is_subgroup(N, G))
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if h1:
            h2 = is_normal(N, G)
    except Exception:
        h2 = False

    # H3: G = MN
    try:
        h3 = False
        if h1:
            int_order = intersect_order(M, N)
            h3 = (get_order(M) * get_order(N) // int_order) == get_order(G)
    except Exception:
        h3 = False

    # Conclusion: G/(M \cap N) \cong (G/M) \times (G/N)
    # The conclusion is a statement about group isomorphism.
    # If M is not normal, G/M is not a group, so the RHS is undefined/not a group,
    # and thus cannot be isomorphic to the LHS as groups.
    # If both M and N are normal, the natural map is an isomorphism iff G = MN.
    try:
        neg_q = False
        if h1:
            if not (is_normal(M, G) and is_normal(N, G)):
                neg_q = True
            else:
                int_order = intersect_order(M, N)
                is_surjective = (get_order(M) * get_order(N) // int_order) == get_order(G)
                neg_q = not is_surjective
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]