import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, N, M = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group, N and M are subgroups of G
    try:
        h1 = isinstance(G, PermutationGroup) and \
             isinstance(N, PermutationGroup) and \
             isinstance(M, PermutationGroup) and \
             N.is_subgroup(G) and \
             M.is_subgroup(G)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = N.is_normal(G)
    except Exception:
        h2 = False

    # H3: The intersection of N and M contains only the identity element
    try:
        try:
            n_elems = list(N.elements)
        except Exception:
            n_elems = list(N.generate())
            
        count = sum(1 for x in n_elems if x in M)
        h3 = (count == 1)
    except Exception:
        h3 = False

    # neg_Q: There exists n in N and m in M such that nm != mn
    try:
        try:
            n_elems = list(N.elements)
        except Exception:
            n_elems = list(N.generate())
            
        try:
            m_elems = list(M.elements)
        except Exception:
            m_elems = list(M.generate())
            
        neg_q = False
        for n in n_elems:
            for m in m_elems:
                if n * m != m * n:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group and N, M are subgroups of G",
    "H_2: N is a normal subgroup of G",
    "H_3: The intersection of N and M contains only the identity element",
    "¬Q: There exists n in N and m in M such that nm != mn"
]

N_HYP = 3
NEG_Q_INDEX = 3