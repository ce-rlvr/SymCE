import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def is_id(p):
    """Check if a permutation is the identity."""
    return len(p.support()) == 0

def is_normal(G, M):
    """Check if M is a normal subgroup of G."""
    for gen in M.generators:
        if not G.contains(gen):
            return False
    for g in G.generators:
        for m in M.generators:
            if not M.contains(g * m * ~g):
                return False
            if not M.contains(~g * m * g):
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, M = witness
    except Exception:
        return [False, False]
        
    # H1: M is a minimal normal subgroup of G
    try:
        h1 = False
        if M.order() > 1 and is_normal(G, M):
            is_minimal = True
            for x in M.generate():
                if is_id(x):
                    continue
                # Compute the normal closure of x in G
                N_gens = [x]
                N_group = PermutationGroup(N_gens)
                while True:
                    added = False
                    for g in G.generators:
                        for h in N_gens:
                            conj1 = g * h * ~g
                            if not N_group.contains(conj1):
                                N_gens.append(conj1)
                                N_group = PermutationGroup(N_gens)
                                added = True
                            conj2 = ~g * h * g
                            if not N_group.contains(conj2):
                                N_gens.append(conj2)
                                N_group = PermutationGroup(N_gens)
                                added = True
                    if not added:
                        break
                # If the normal closure of any non-identity element is strictly smaller than M,
                # then M is not a minimal normal subgroup.
                if N_group.order() < M.order():
                    is_minimal = False
                    break
            h1 = is_minimal
    except Exception:
        h1 = False
        
    # neg_Q: M is NOT a direct factor of G
    try:
        neg_q = False
        if not is_normal(G, M):
            neg_q = True
        elif G.order() % M.order() != 0:
            neg_q = True
        else:
            target_order = G.order() // M.order()
            elements = list(G.generate())
            
            # Compute all conjugacy classes of G
            classes = []
            seen = set()
            for x in elements:
                if x in seen:
                    continue
                cclass = set()
                for g in elements:
                    cclass.add(g * x * ~g)
                classes.append(list(cclass))
                seen.update(cclass)
                
            id_class = None
            other_classes = []
            for c in classes:
                if is_id(c[0]):
                    id_class = c
                else:
                    other_classes.append(c)
                    
            if id_class is None:
                neg_q = False
            else:
                target_rem = target_order - len(id_class)
                if target_rem < 0:
                    neg_q = True
                elif target_rem == 0:
                    # The trivial subgroup is a valid complement
                    neg_q = False
                else:
                    valid_K_found = False
                    
                    # Find if any union of conjugacy classes forms a valid complement K
                    def find_subsets(index, current_sum, current_subset):
                        nonlocal valid_K_found
                        if valid_K_found:
                            return
                        if current_sum == target_rem:
                            K_elements = set(id_class)
                            for c in current_subset:
                                K_elements.update(c)
                            
                            # Check if K_elements is closed under multiplication (forms a subgroup)
                            is_subgroup = True
                            K_list = list(K_elements)
                            for a in K_list:
                                for b in K_list:
                                    if a * b not in K_elements:
                                        is_subgroup = False
                                        break
                                if not is_subgroup:
                                    break
                            
                            if is_subgroup:
                                # Check if M \cap K = {1}
                                intersection_trivial = True
                                for m in M.generate():
                                    if not is_id(m) and m in K_elements:
                                        intersection_trivial = False
                                        break
                                if intersection_trivial:
                                    valid_K_found = True
                            return
                            
                        if index >= len(other_classes):
                            return
                            
                        # Include the current class
                        if current_sum + len(other_classes[index]) <= target_rem:
                            find_subsets(index + 1, current_sum + len(other_classes[index]), current_subset + [other_classes[index]])
                            
                        # Exclude the current class
                        find_subsets(index + 1, current_sum, current_subset)

                    find_subsets(0, 0, [])
                    neg_q = not valid_K_found
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a minimal normal subgroup of G",
    "¬Q: M is not a direct factor of G"
]

N_HYP = 1
NEG_Q_INDEX = 1