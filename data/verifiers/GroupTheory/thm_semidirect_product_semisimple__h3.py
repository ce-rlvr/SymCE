import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    def get_elements(grp):
        if not hasattr(grp, "_elements_set"):
            elems = set()
            for i, el in enumerate(grp.generate()):
                if i > 20000:
                    raise ValueError("Group too large")
                elems.add(el)
            grp._elements_set = elems
        return grp._elements_set

    def is_subgroup(sub, grp):
        try:
            grp_elems = get_elements(grp)
            return all(gen in grp_elems for gen in sub.generators)
        except Exception:
            return False

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1_ok = False
        
    # H_2: G is a semisimple group (has no non-trivial abelian normal subgroups)
    try:
        def is_semisimple(grp):
            if grp.order() == 1:
                return True
            id_el = grp.identity
            checked = {id_el}
            gens_and_invs = grp.generators + [~x for x in grp.generators]
            
            for g in get_elements(grp):
                if g in checked:
                    continue
                    
                seen = {g}
                queue = [g]
                while queue:
                    curr = queue.pop(0)
                    for gen in gens_and_invs:
                        conj = gen * curr * ~gen
                        if conj not in seen:
                            seen.add(conj)
                            queue.append(conj)
                            
                checked.update(seen)
                
                # If all elements in the conjugacy class commute, 
                # its normal closure is an abelian normal subgroup.
                seen_list = list(seen)
                is_ab = True
                for i in range(len(seen_list)):
                    for j in range(i + 1, len(seen_list)):
                        if seen_list[i] * seen_list[j] != seen_list[j] * seen_list[i]:
                            is_ab = False
                            break
                    if not is_ab:
                        break
                        
                if is_ab:
                    return False
            return True
            
        h2_ok = is_semisimple(G)
    except Exception:
        h2_ok = False
        
    # H_3: H is a subgroup of G such that G is the internal semidirect product of N and H
    try:
        def is_internal_semidirect_product(grp, n_grp, h_grp):
            if not is_subgroup(n_grp, grp): return False
            if not is_subgroup(h_grp, grp): return False
            
            n_elements = get_elements(n_grp)
            h_elements = get_elements(h_grp)
            
            # N must be normal in G
            for g in grp.generators:
                for n in n_grp.generators:
                    if g * n * ~g not in n_elements:
                        return False
                        
            # Intersection must be trivial
            if len(n_elements.intersection(h_elements)) != 1:
                return False
                
            # N * H = G
            if n_grp.order() * h_grp.order() != grp.order():
                return False
                
            return True
            
        h3_ok = is_internal_semidirect_product(G, N, H)
    except Exception:
        h3_ok = False
        
    # ¬Q: H is NOT a normal subgroup of G (so G is not the internal direct product of N and H)
    try:
        def is_normal(grp, subgrp):
            sub_elements = get_elements(subgrp)
            for g in grp.generators:
                for s in subgrp.generators:
                    if g * s * ~g not in sub_elements:
                        return False
            return True
            
        neg_q_ok = not is_normal(G, H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: H is a subgroup of G such that G is the internal semidirect product of N and H",
    "¬Q: H is not a normal subgroup of G (so G is not the internal direct product of N and H)"
]

N_HYP = 3
NEG_Q_INDEX = 3