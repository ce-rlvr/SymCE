import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_automorphisms(G):
    elements = list(G.elements)
    identity = next(e for e in elements if e * e == e)
    gens = G.generators
    auts = []
    
    for target in itertools.product(elements, repeat=len(gens)):
        try:
            if any(g.order() != t.order() for g, t in zip(gens, target)):
                continue
        except Exception:
            pass
            
        mapping = {identity: identity}
        for g, t in zip(gens, target):
            mapping[g] = t
            
        queue = [identity] + list(gens)
        valid = True
        
        while queue:
            curr = queue.pop(0)
            for i, g in enumerate(gens):
                nxt = curr * g
                mapped_nxt = mapping[curr] * target[i]
                if nxt in mapping:
                    if mapping[nxt] != mapped_nxt:
                        valid = False
                        break
                else:
                    mapping[nxt] = mapped_nxt
                    queue.append(nxt)
            if not valid:
                break
                
        if valid and len(mapping) == len(elements):
            if len(set(mapping.values())) == len(elements):
                auts.append(mapping)
                
    return auts

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, C = witness
        else:
            G, C = None, None
    except Exception:
        G, C = None, None

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            elements = list(G.elements)
            is_valid_C = True
            C_sets = []
            for K in C:
                try:
                    K_set = frozenset(K)
                    for k in K_set:
                        if k not in elements:
                            is_valid_C = False
                            break
                    if not is_valid_C:
                        break
                    C_sets.append(K_set)
                except Exception:
                    is_valid_C = False
                    break
            
            if not is_valid_C:
                neg_q = False
            else:
                auts = get_automorphisms(G)
                action_well_defined = True
                C_sets_set = set(C_sets)
                for phi in auts:
                    for K in C_sets:
                        mapped_K = frozenset(phi[k] for k in K)
                        if mapped_K not in C_sets_set:
                            action_well_defined = False
                            break
                    if not action_well_defined:
                        break
                neg_q = not action_well_defined
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Aut(G) is the group of automorphisms of G",
    "¬Q: The map Aut(G) x C -> C is not a well-defined group action"
]

N_HYP = 2
NEG_Q_INDEX = 2