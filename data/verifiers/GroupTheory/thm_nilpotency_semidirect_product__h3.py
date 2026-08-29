import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: N is a finite group and G is a semidirect product of N and H",
    "H_2: H is a finite group",
    "¬Q: The equivalence between G being nilpotent and (G is a direct product and N, H are nilpotent) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness (G, N, H), checks if it is a valid counterexample.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    def is_subgroup(group, sub):
        for g in sub.generators:
            if g not in group:
                return False
        return True

    def is_normal_subgroup(group, sub):
        if not is_subgroup(group, sub):
            return False
        for n in sub.generators:
            for g in group.generators:
                if (g * n * ~g) not in sub:
                    return False
                if (~g * n * g) not in sub:
                    return False
        return True

    def check_nilpotent(group):
        nilp = group.is_nilpotent
        if callable(nilp):
            return nilp()
        return nilp

    def get_order(group):
        order = group.order
        if callable(order):
            return order()
        return order

    def get_elements(group):
        if hasattr(group, 'elements'):
            el = group.elements
            if callable(el):
                return list(el())
            if isinstance(el, (list, set, tuple)):
                return list(el)
        return list(group.generate())

    # H1: N is a finite group (and G is a semidirect product of N and H)
    try:
        if not (isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup)):
            h1 = False
        else:
            is_sdp = True
            if not is_subgroup(G, N):
                is_sdp = False
            elif not is_subgroup(G, H):
                is_sdp = False
            elif not is_normal_subgroup(G, N):
                is_sdp = False
            elif get_order(N) * get_order(H) != get_order(G):
                is_sdp = False
            else:
                for g in get_elements(N):
                    is_id = getattr(g, 'is_Identity', False)
                    if not is_id and hasattr(G, 'identity'):
                        is_id = (g == G.identity)
                    if not is_id:
                        if g in H:
                            is_sdp = False
                            break
            h1 = is_sdp
    except Exception:
        h1 = False

    # H2: H is a finite group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # neg_Q: G is nilpotent iff (direct product and N nilpotent and H nilpotent)
    try:
        g_nilp = bool(check_nilpotent(G))
        n_nilp = bool(check_nilpotent(N))
        h_nilp = bool(check_nilpotent(H))
        is_dp = bool(is_normal_subgroup(G, H))
        
        rhs = is_dp and n_nilp and h_nilp
        q = (g_nilp == rhs)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]