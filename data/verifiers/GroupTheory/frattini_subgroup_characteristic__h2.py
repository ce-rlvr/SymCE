import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def frattini_subgroup_elements(G):
    elements = list(G.generate())
    id_el = None
    for e in elements:
        if e * e == e:
            id_el = e
            break
            
    if len(elements) == 1:
        return set([id_el])
        
    seen = {frozenset([id_el])}
    queue = [set([id_el])]
    
    while queue:
        H = queue.pop(0)
        for x in elements:
            if x not in H:
                new_H = set(H)
                frontier = [x]
                new_H.add(x)
                while frontier:
                    y = frontier.pop()
                    for z in list(new_H):
                        yz = y * z
                        if yz not in new_H:
                            new_H.add(yz)
                            frontier.append(yz)
                        zy = z * y
                        if zy not in new_H:
                            new_H.add(zy)
                            frontier.append(zy)
                fs = frozenset(new_H)
                if fs not in seen:
                    seen.add(fs)
                    queue.append(new_H)
                    
    all_subs = list(seen)
    proper_subs = [s for s in all_subs if len(s) < len(elements)]
    
    if not proper_subs:
        return set(elements)
        
    maximal_subs = []
    for s in proper_subs:
        is_maximal = True
        for other in proper_subs:
            if s != other and s.issubset(other):
                is_maximal = False
                break
        if is_maximal:
            maximal_subs.append(s)
            
    if not maximal_subs:
        return set(elements)
        
    frattini = set(maximal_subs[0])
    for m in maximal_subs[1:]:
        frattini = frattini.intersection(m)
        
    return frattini

def is_characteristic(G, H_elements):
    elements = list(G.generate())
    id_el = None
    for e in elements:
        if e * e == e:
            id_el = e
            break
            
    gens = G.generators
    
    for target_gens in itertools.product(elements, repeat=len(gens)):
        gen_set = set([id_el])
        q = list(target_gens)
        for tg in target_gens:
            gen_set.add(tg)
            
        while q:
            y = q.pop(0)
            for z in list(gen_set):
                yz = y * z
                if yz not in gen_set:
                    gen_set.add(yz)
                    q.append(yz)
                zy = z * y
                if zy not in gen_set:
                    gen_set.add(zy)
                    q.append(zy)
                    
        if len(gen_set) < len(elements):
            continue
            
        mapping = {id_el: id_el}
        is_valid = True
        for g, tg in zip(gens, target_gens):
            if g in mapping and mapping[g] != tg:
                is_valid = False
            mapping[g] = tg
            
        if not is_valid:
            continue
            
        q = [id_el]
        for g in gens:
            if g not in q:
                q.append(g)
                
        while q and is_valid:
            curr = q.pop(0)
            for g, tg in zip(gens, target_gens):
                nxt = curr * g
                mapped_nxt = mapping[curr] * tg
                if nxt in mapping:
                    if mapping[nxt] != mapped_nxt:
                        is_valid = False
                        break
                else:
                    mapping[nxt] = mapped_nxt
                    q.append(nxt)
                    
        if not is_valid:
            continue
            
        mapped_H = {mapping[h] for h in H_elements}
        if mapped_H != H_elements:
            return False
            
    return True

def conditions(witness):
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False
        
    try:
        if not h1_ok:
            neg_q = False
        else:
            gen = witness.generate()
            count = 0
            for _ in gen:
                count += 1
                if count > 100:
                    break
            if count > 100:
                neg_q = False
            else:
                phi_elements = frattini_subgroup_elements(witness)
                neg_q = not is_characteristic(witness, phi_elements)
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: \\Phi(G) is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1