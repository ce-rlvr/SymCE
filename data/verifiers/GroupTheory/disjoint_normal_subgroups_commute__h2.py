import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, M) where G is a PermutationGroup,
    and N, M are subsets or subgroups of G.
    """
    try:
        G, N, M = witness
    except Exception:
        return [False, False, False, False]

    def normalize_perms(perms, target_size):
        normalized = set()
        for p in perms:
            if not isinstance(p, Permutation):
                normalized.add(p)
                continue
            if p.size < target_size:
                arr = p.array_form + list(range(p.size, target_size))
                normalized.add(Permutation(arr))
            elif p.size == target_size:
                normalized.add(p)
            else:
                if any(p(i) != i for i in range(target_size, p.size)):
                    normalized.add(p)
                else:
                    normalized.add(Permutation(p.array_form[:target_size]))
        return normalized

    def get_raw_elems(X):
        if isinstance(X, PermutationGroup):
            return set(X.elements)
        try:
            return set(X)
        except Exception:
            return set()

    n_raw = get_raw_elems(N)
    m_raw = get_raw_elems(M)

    # H1: G is a group, N and M are subsets of G
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            target_size = G.degree
            n_elems_h1 = normalize_perms(n_raw, target_size)
            m_elems_h1 = normalize_perms(m_raw, target_size)
            g_elems = set(G.elements)
            h1 = n_elems_h1.issubset(g_elems) and m_elems_h1.issubset(g_elems)
    except Exception:
        h1 = False

    # H2: M is a normal subgroup of G
    try:
        h2 = False
        if isinstance(G, PermutationGroup):
            target_size = G.degree
            m_elems_h2 = normalize_perms(m_raw, target_size)
            g_elems = set(G.elements)
            if m_elems_h2 and m_elems_h2.issubset(g_elems):
                # Check if M is a subgroup (closed under multiplication)
                is_subgroup = True
                for m1 in m_elems_h2:
                    for m2 in m_elems_h2:
                        if m1 * m2 not in m_elems_h2:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                # Check normality
                if is_subgroup:
                    is_normal = True
                    for g in g_elems:
                        g_inv = ~g
                        for m in m_elems_h2:
                            if g * m * g_inv not in m_elems_h2:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                    h2 = is_normal
    except Exception:
        h2 = False

    # H3: The intersection of N and M contains only the identity element
    try:
        h3 = False
        if isinstance(G, PermutationGroup):
            target_size = G.degree
            n_elems_h3 = normalize_perms(n_raw, target_size)
            m_elems_h3 = normalize_perms(m_raw, target_size)
            intersection = n_elems_h3.intersection(m_elems_h3)
            h3 = (intersection == {G.identity})
    except Exception:
        h3 = False

    # neg_Q: There exists n in N and m in M such that nm != mn
    try:
        neg_q = False
        for n in n_raw:
            for m in m_raw:
                if isinstance(n, Permutation) and isinstance(m, Permutation):
                    if n * m != m * n:
                        neg_q = True
                        break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and N, M are subsets of G",
    "H_2: M is a normal subgroup of G",
    "H_3: The intersection of N and M contains only the identity element",
    "¬Q: There exist n in N and m in M such that nm != mn"
]

N_HYP = 3
NEG_Q_INDEX = 3