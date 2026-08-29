import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

# Top-level setup
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Q8 = PermutationGroup(Permutation([[0, 1, 2, 3], [4, 5, 6, 7]]), Permutation([[0, 4, 2, 6], [1, 7, 3, 5]]))

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False, False]
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group (and P is a subgroup of G)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup) and P.is_subgroup(G)
    except Exception:
        try:
            h1 = isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup) and all(gen in G for gen in P.generators)
        except Exception:
            h1 = False

    # H_2: p is a prime number dividing the order of G
    try:
        h2 = isinstance(p, int) and isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False

    # H_3: P is contained in the center of its normalizer N_G(P)
    try:
        if h1:
            P_gens = P.generators
            N_G_P = []
            for g in G.elements:
                normalizes = True
                for x in P_gens:
                    if (g * x * ~g) not in P:
                        normalizes = False
                        break
                if normalizes:
                    N_G_P.append(g)
            
            h3 = True
            for x in P_gens:
                for n in N_G_P:
                    if x * n != n * x:
                        h3 = False
                        break
                if not h3:
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: G does not have a normal p-complement
    try:
        if h1:
            order_G = G.order()
            order_P = P.order()
            if order_G % order_P != 0:
                neg_q = True
            else:
                target_order = order_G // order_P
                
                elements = list(G.elements)
                identity = elements[0]**0
                classes = []
                seen = set()
                for x in elements:
                    if x in seen:
                        continue
                    cclass = set()
                    for g in elements:
                        cclass.add(g * x * ~g)
                    classes.append(cclass)
                    seen.update(cclass)
                
                other_classes = [c for c in classes if identity not in c]
                other_classes.sort(key=len, reverse=True)
                target_sum = target_order - 1
                
                suffix_sums = [0] * len(other_classes)
                if other_classes:
                    suffix_sums[-1] = len(other_classes[-1])
                    for i in range(len(other_classes)-2, -1, -1):
                        suffix_sums[i] = suffix_sums[i+1] + len(other_classes[i])
                
                has_complement = False
                P_elements = set(P.elements)
                
                def check_union(union):
                    N_elements = set([identity])
                    for c in union:
                        N_elements.update(c)
                    
                    is_subgroup = True
                    N_list = list(N_elements)
                    for i in range(len(N_list)):
                        for j in range(i, len(N_list)):
                            if N_list[i] * N_list[j] not in N_elements:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                            
                    if is_subgroup:
                        intersection = P_elements.intersection(N_elements)
                        if len(intersection) == 1:
                            return True
                    return False

                def find_combinations(idx, current_sum, current_union):
                    nonlocal has_complement
                    if has_complement:
                        return
                    if current_sum == target_sum:
                        if check_union(current_union):
                            has_complement = True
                        return
                    if current_sum > target_sum or idx >= len(other_classes):
                        return
                    if current_sum + suffix_sums[idx] < target_sum:
                        return
                    
                    find_combinations(idx + 1, current_sum + len(other_classes[idx]), current_union + [other_classes[idx]])
                    find_combinations(idx + 1, current_sum, current_union)

                find_combinations(0, 0, [])
                neg_q = not has_complement
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: P is contained in the center of its normalizer N_G(P)",
    "¬Q: G does not have a normal p-complement"
]

N_HYP = 3
NEG_Q_INDEX = 3