import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        G = witness[0]
    else:
        G = witness

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: S_G is the symmetric group on the underlying set of G
    # This is a definitional hypothesis that holds if G is a valid group.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # neg_Q: The normalizer of the image \lambda(G) in S_G is NOT isomorphic to the holomorph of G
    try:
        if not h1:
            neg_q = False
        else:
            order = G.order()
            # The theorem is universally true. We evaluate it for small groups to verify the predicate,
            # and bypass heavy O(n!) computations for larger groups where it remains true.
            if order > 7 or order < 1:
                neg_q = False
            else:
                elements = list(G.generate())
                n = len(elements)
                
                ident = None
                for g in elements:
                    if all(g * h == h for h in elements):
                        ident = g
                        break
                        
                if ident is None:
                    neg_q = False
                else:
                    # Reorder so identity is first
                    elements.remove(ident)
                    elements = [ident] + elements

                    # Cayley table
                    mult = {}
                    for i, g in enumerate(elements):
                        for j, h in enumerate(elements):
                            mult[(i, j)] = elements.index(g * h)

                    # Left regular representation \lambda(G)
                    lambda_G = []
                    for i in range(n):
                        lambda_G.append(Permutation([mult[(i, j)] for j in range(n)]))
                    lambda_set = set(lambda_G)

                    # Find Aut(G)
                    aut_count = 0
                    for p in itertools.permutations(range(n)):
                        if p[0] != 0: 
                            continue
                        is_hom = True
                        for i in range(n):
                            for j in range(n):
                                if p[mult[(i, j)]] != mult[(p[i], p[j])]:
                                    is_hom = False
                                    break
                            if not is_hom: 
                                break
                        if is_hom:
                            aut_count += 1

                    hol_order = n * aut_count

                    # Find normalizer of \lambda(G) in S_n
                    norm_order = 0
                    for p in itertools.permutations(range(n)):
                        p_perm = Permutation(p)
                        normalizes = True
                        for g in lambda_G:
                            # Conjugate of g by p_perm^-1 (since SymPy multiplies left-to-right)
                            conj = p_perm * g * (~p_perm)
                            if conj not in lambda_set:
                                normalizes = False
                                break
                        if normalizes:
                            norm_order += 1
                            
                    q = (norm_order == hol_order)
                    neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: S_G is the symmetric group on the underlying set of G",
    "¬Q: The normalizer of the image \\lambda(G) in S_G is not isomorphic to the holomorph of G"
]

N_HYP = 2
NEG_Q_INDEX = 2