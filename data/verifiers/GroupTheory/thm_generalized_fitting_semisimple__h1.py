import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import combinations

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_conjugacy_classes(G, elements):
    classes = []
    seen = set()
    gens = G.generators
    gen_invs = [~g for g in gens]
    for g in elements:
        if g in seen:
            continue
        c = set([g])
        frontier = [g]
        while frontier:
            curr = frontier.pop()
            for i in range(len(gens)):
                gen = gens[i]
                gen_inv = gen_invs[i]
                # Conjugate by generator
                conj1 = gen * curr * gen_inv
                if conj1 not in c:
                    c.add(conj1)
                    frontier.append(conj1)
                # Conjugate by inverse of generator
                conj2 = gen_inv * curr * gen
                if conj2 not in c:
                    c.add(conj2)
                    frontier.append(conj2)
        classes.append(list(c))
        seen.update(c)
    return classes

def get_normal_subgroups_elements(G, elements, identity):
    classes = get_conjugacy_classes(G, elements)
        
    id_class_idx = -1
    for i, c in enumerate(classes):
        if identity in c:
            id_class_idx = i
            break
            
    normal_subgroups_elements = []
    order_G = len(elements)
    other_classes = [i for i in range(len(classes)) if i != id_class_idx]
    
    for r in range(len(other_classes) + 1):
        for combo in combinations(other_classes, r):
            subset_indices = [id_class_idx] + list(combo)
            size = sum(len(classes[i]) for i in subset_indices)
            if order_G % size != 0:
                continue
                
            subset_elements = set()
            for i in subset_indices:
                subset_elements.update(classes[i])
                
            is_closed = True
            for i in subset_indices:
                rep = classes[i][0]
                for x in subset_elements:
                    if rep * x not in subset_elements:
                        is_closed = False
                        break
                if not is_closed:
                    break
                    
            if is_closed:
                normal_subgroups_elements.append(subset_elements)
                
    return normal_subgroups_elements

def generate_subgroup(generators, identity):
    group = set([identity])
    if not generators:
        return group
    frontier = list(generators)
    group.update(generators)
    while frontier:
        curr = frontier.pop()
        for g in generators:
            p1 = curr * g
            if p1 not in group:
                group.add(p1)
                frontier.append(p1)
            p2 = g * curr
            if p2 not in group:
                group.add(p2)
                frontier.append(p2)
    return group

def is_nilpotent_group(elements_set, identity):
    current_L = elements_set
    while len(current_L) > 1:
        commutators = set()
        for a in current_L:
            for b in elements_set:
                commutators.add(~a * ~b * a * b)
        next_L = generate_subgroup(commutators, identity)
        if len(next_L) == len(current_L):
            return False
        current_L = next_L
    return True

def get_fitting_subgroup(normal_subgroups_elements, identity):
    max_nilp = set([identity])
    for N in normal_subgroups_elements:
        if len(N) > len(max_nilp) and is_nilpotent_group(N, identity):
            max_nilp = N
    return max_nilp

def get_socle_elements(identity, normal_subgroups_elements):
    nontrivial = [N for N in normal_subgroups_elements if len(N) > 1]
    minimal = []
    for N in nontrivial:
        is_minimal = True
        for M in nontrivial:
            if len(M) < len(N) and M.issubset(N):
                is_minimal = False
                break
        if is_minimal:
            minimal.append(N)
            
    if not minimal:
        return set([identity])
        
    socle = set([identity])
    for M in minimal:
        new_socle = set()
        for x in socle:
            for y in M:
                new_socle.add(x * y)
        socle = new_socle
        
    return socle

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False]
            
        elements = list(witness.generate())
        if not elements:
            return [False, False]
            
        identity = None
        for e in elements:
            if e * e == e:
                identity = e
                break
        if identity is None:
            return [False, False]
            
        normal_subgroups_elements = get_normal_subgroups_elements(witness, elements, identity)
        
        # The Fitting subgroup F(G) is the join of all nilpotent normal subgroups.
        # G is semisimple iff F(G) is trivial.
        F_G = get_fitting_subgroup(normal_subgroups_elements, identity)
        is_semi = (len(F_G) == 1)
        
        # For a semisimple group, F^*(G) = Socle(G).
        # The conjecture states F^*(G) = G.
        if is_semi:
            socle = get_socle_elements(identity, normal_subgroups_elements)
            neg_q = len(socle) != len(elements)
        else:
            # Fallback for non-semisimple witnesses (which fail H_1 anyway)
            if len(F_G) == len(elements):
                neg_q = False
            else:
                neg_q = True
                
        return [is_semi, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "¬Q: The generalized Fitting subgroup F^*(G) of G is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1