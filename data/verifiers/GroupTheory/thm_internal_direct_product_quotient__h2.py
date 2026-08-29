import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
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
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        from sympy.combinatorics import PermutationGroup
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup) or not isinstance(K, PermutationGroup):
            h1 = False
        else:
            h1 = all(G.contains(g) for g in H.generators) and all(G.contains(g) for g in K.generators)
    except Exception:
        h1 = False

    def get_order(group):
        return group.order() if callable(group.order) else group.order

    def get_elements(group):
        return group.elements() if callable(group.elements) else group.elements

    try:
        order_H = get_order(H)
        order_K = get_order(K)
        order_G = get_order(G)
        
        if order_H < order_K:
            A, B = H, K
        else:
            A, B = K, H
        
        intersection_size = 0
        for g in get_elements(A):
            if B.contains(g):
                intersection_size += 1
    except Exception:
        intersection_size = -1

    try:
        h2 = (intersection_size == 1)
    except Exception:
        h2 = False

    try:
        if intersection_size > 0:
            h3 = (order_H * order_K // intersection_size == order_G)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        def is_normal(group, sub):
            for g in group.generators:
                for h in sub.generators:
                    if not sub.contains(g * h * ~g):
                        return False
                    if not sub.contains(~g * h * g):
                        return False
            return True

        # If H is not normal in G, G/H is not a group, so G/H ≅ K is false.
        if not is_normal(G, H):
            neg_q = True
        else:
            from sympy.combinatorics import Permutation, PermutationGroup, CyclicGroup
            
            # Construct H x K
            gens = []
            deg_H = H.degree
            deg_K = K.degree
            for g in H.generators:
                arr = g.array_form
                if len(arr) < deg_H:
                    arr = arr + list(range(len(arr), deg_H))
                arr = arr + list(range(deg_H, deg_H + deg_K))
                gens.append(Permutation(arr))
            for g in K.generators:
                arr = g.array_form
                if len(arr) < deg_K:
                    arr = arr + list(range(len(arr), deg_K))
                arr = list(range(deg_H)) + [i + deg_H for i in arr]
                gens.append(Permutation(arr))
            
            if not gens:
                HxK = CyclicGroup(1)
            else:
                HxK = PermutationGroup(gens)
            
            isomo_HxK = G.is_isomorphic(HxK)

            # Construct G/H
            coset_reps = []
            for g in get_elements(G):
                found = False
                for rep in coset_reps:
                    if H.contains(g * ~rep):
                        found = True
                        break
                if not found:
                    coset_reps.append(g)
            
            q_gens = []
            for g in G.generators:
                perm = []
                for i in range(len(coset_reps)):
                    target = coset_reps[i] * g
                    for j in range(len(coset_reps)):
                        if H.contains(target * ~coset_reps[j]):
                            perm.append(j)
                            break
                q_gens.append(Permutation(perm))
            
            if not q_gens:
                G_mod_H = CyclicGroup(1)
            else:
                G_mod_H = PermutationGroup(q_gens)
            
            isomo_quotient = G_mod_H.is_isomorphic(K)

            neg_q = not (isomo_HxK and isomo_quotient)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group (and H, K are subgroups)",
    "H_2: H ∩ K = {e}",
    "H_3: HK = G",
    "¬Q: G is not isomorphic to H × K or G/H is not isomorphic to K"
]

N_HYP = 3
NEG_Q_INDEX = 3