import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, A, x = witness
            elif len(witness) == 2:
                G, A = witness
                x = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def get_order(grp):
        if callable(grp.order):
            return grp.order()
        return grp.order

    def check_abelian(grp):
        if callable(grp.is_abelian):
            return grp.is_abelian()
        return grp.is_abelian

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1 and isinstance(A, PermutationGroup):
            is_sub = all(G.contains(g) for g in A.generators)
            if is_sub:
                if check_abelian(A):
                    is_norm = True
                    for g in G.generators:
                        g_inv = ~g
                        for a in A.generators:
                            if not A.contains(g * a * g_inv):
                                is_norm = False
                                break
                        if not is_norm:
                            break
                    h2 = is_norm
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and h2:
            index = get_order(G) // get_order(A)
            
            def conj_class_size(G, elem):
                orbit = set()
                queue = [elem]
                orbit.add(elem)
                while queue:
                    curr = queue.pop(0)
                    for g in G.generators:
                        nxt = g * curr * (~g)
                        if nxt not in orbit:
                            orbit.add(nxt)
                            queue.append(nxt)
                return len(orbit)
            
            if x is not None:
                if G.contains(x):
                    c_size = conj_class_size(G, x)
                    neg_q = (index % c_size != 0)
            else:
                for elem in G.generate():
                    c_size = conj_class_size(G, elem)
                    if index % c_size != 0:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: A is an abelian normal subgroup of G",
    "not Q: The size of the conjugacy class of x in G does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2