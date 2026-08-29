import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def is_characteristic(G, P):
    elements = list(G.generate())
    n = len(elements)
    idx = {e: i for i, e in enumerate(elements)}
    table = [[idx[e1 * e2] for e2 in elements] for e1 in elements]
    
    gens = G.generators
    gen_indices = [idx[g] for g in gens]
    
    P_elements = set(P.generate())
    P_indices = {idx[e] for e in P_elements}
    
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
    if id_elem is None:
        return False
    id_idx = idx[id_elem]
    
    for p_gens in itertools.product(range(n), repeat=len(gens)):
        H = PermutationGroup([elements[i] for i in p_gens])
        if H.order() == n:
            mapping = {id_idx: id_idx}
            conflict = False
            for i, gi in enumerate(gen_indices):
                if gi in mapping:
                    if mapping[gi] != p_gens[i]:
                        conflict = True
                        break
                else:
                    mapping[gi] = p_gens[i]
            
            if conflict:
                continue
                
            queue = list(mapping.keys())
            valid = True
            head = 0
            while head < len(queue):
                u = queue[head]
                head += 1
                for i, gi in enumerate(gen_indices):
                    v = table[u][gi]
                    mapped_v = table[mapping[u]][mapping[gi]]
                    if v in mapping:
                        if mapping[v] != mapped_v:
                            valid = False
                            break
                    else:
                        mapping[v] = mapped_v
                        queue.append(v)
                if not valid:
                    break
            
            if valid and len(mapping) == n:
                for p_idx in P_indices:
                    if mapping[p_idx] not in P_indices:
                        return False
    return True

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        else:
            P_elements = set(P.generate())
            G_elements = set(G.generate())
            if not P_elements.issubset(G_elements):
                h3 = False
            else:
                h3 = True
                for g in G.generators:
                    for h in P.generators:
                        if (g * h * (~g)) not in P_elements or ((~g) * h * g) not in P_elements:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False
        
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            neg_q = not is_characteristic(G, P)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a normal subgroup of G",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3