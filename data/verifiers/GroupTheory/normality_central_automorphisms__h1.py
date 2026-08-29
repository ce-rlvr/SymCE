import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_center(G, elements):
    center = set()
    for x in elements:
        is_central = True
        for y in elements:
            if x * y != y * x:
                is_central = False
                break
        if is_central:
            center.add(x)
    return center

def get_automorphisms(G, elements):
    gens = G.generators
    n_gens = len(gens)
    n = len(elements)
    
    word_for = {}
    word_for[G.identity] = []
    queue = [G.identity]
    while queue:
        curr = queue.pop(0)
        for i, g in enumerate(gens):
            nxt = curr * g
            if nxt not in word_for:
                word_for[nxt] = word_for[curr] + [i]
                queue.append(nxt)
                
    subgroup_sizes = []
    for i in range(1, n_gens + 1):
        sg = PermutationGroup(gens[:i])
        subgroup_sizes.append(sg.order())
        
    elements_by_order = {}
    for x in elements:
        o = x.order()
        if o not in elements_by_order:
            elements_by_order[o] = []
        elements_by_order[o].append(x)
        
    auts = []
    
    def backtrack(gen_idx, current_mapping):
        if gen_idx == n_gens:
            mapping = {}
            for x in elements:
                val = G.identity
                for idx in word_for[x]:
                    val = val * current_mapping[idx]
                mapping[x] = val
            
            if len(set(mapping.values())) != n:
                return
                
            is_hom = True
            for x in gens:
                for y in elements:
                    if mapping[x * y] != mapping[x] * mapping[y]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            if is_hom:
                auts.append(mapping)
            return
            
        g = gens[gen_idx]
        o = g.order()
        candidates = elements_by_order.get(o, [])
        for cand in candidates:
            sg = PermutationGroup(current_mapping + [cand])
            if sg.order() != subgroup_sizes[gen_idx]:
                continue
            
            current_mapping.append(cand)
            backtrack(gen_idx + 1, current_mapping)
            current_mapping.pop()
            
    backtrack(0, [])
    return auts

def get_aut_c(auts, elements, center):
    aut_c = []
    for phi in auts:
        is_c = True
        for x in elements:
            val = (x**-1) * phi[x]
            if val not in center:
                is_c = False
                break
        if is_c:
            aut_c.append(phi)
    return aut_c

def is_normal(auts, aut_c, elements):
    for phi in aut_c:
        for psi in auts:
            psi_inv = {v: k for k, v in psi.items()}
            composed = {}
            for x in elements:
                composed[x] = psi[phi[psi_inv[x]]]
            if composed not in aut_c:
                return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False]
        elements = list(witness.generate())
        if len(elements) < 1:
            return [False, False]
        h1_ok = True
    except Exception:
        return [False, False]
        
    try:
        center = get_center(witness, elements)
        auts = get_automorphisms(witness, elements)
        aut_c = get_aut_c(auts, elements, center)
        
        normal = is_normal(auts, aut_c, elements)
        neg_q = not normal
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Aut_c(G) is defined as the set of central automorphisms",
    "¬Q: Aut_c(G) is not a normal subgroup of Aut(G)"
]
N_HYP = 1
NEG_Q_INDEX = 1