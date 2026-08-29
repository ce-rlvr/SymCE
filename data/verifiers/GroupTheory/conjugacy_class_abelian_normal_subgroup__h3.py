import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            A = witness.get('A')
            a = witness.get('a')
        else:
            G, A, a = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group and a is an element of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(a, Permutation) and G.contains(a)
    except Exception:
        h1 = False

    # H_2: A is an abelian normal subgroup of G
    try:
        if isinstance(A, PermutationGroup):
            h2_subgroup = all(G.contains(g) for g in A.generators)
            h2_abelian = A.is_abelian
            if h2_subgroup:
                h2_normal = all(A.contains(~g * h * g) for g in G.generators for h in A.generators) and \
                            all(A.contains(g * h * ~g) for g in G.generators for h in A.generators)
            else:
                h2_normal = False
            h2 = bool(h2_subgroup and h2_abelian and h2_normal)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The size of the conjugacy class of a in G does not divide the index of A in G
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            conj_class = set()
            for g in G.generate():
                conj_class.add(~g * a * g)
            c_size = len(conj_class)
            
            index = G.order() // A.order()
            
            neg_q = bool(index % c_size != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and a is an element of G",
    "H_2: A is an abelian normal subgroup of G",
    "¬Q: The size of the conjugacy class of a in G does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2