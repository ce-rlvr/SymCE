import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for standard groups
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_aut_and_inn(G):
    if G.order() > 60:
        raise ValueError("Group too large for fast automorphism computation")
    
    elements = list(G.generate())
    n = len(elements)
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    # Precompute multiplication table
    mult_table = [[0]*n for _ in range(n)]
    for i, x in enumerate(elements):
        for j, y in enumerate(elements):
            mult_table[i][j] = elem_to_idx[x * y]
            
    # Compute Inner Automorphisms: Inn(G)
    inn_perms = []
    for g in elements:
        perm = []
        g_inv = ~g
        for x in elements:
            y = g * x * g_inv
            perm.append(elem_to_idx[y])
        inn_perms.append(Permutation(perm))
    InnG = PermutationGroup(inn_perms)
    
    # Compute Full Automorphism Group: Aut(G)
    gens = G.generators
    gen_indices = [elem_to_idx[g] for g in gens]
    gen_orders = [g.order() for g in gens]
    
    candidates = []
    for order in gen_orders:
        cands = [i for i, e in enumerate(elements) if e.order() == order]
        candidates.append(cands)
        
    identity = None
    for e in elements:
        if e.order() == 1:
            identity = e
            break
            
    # Build words for each element using BFS on the Cayley graph
    words = {elem_to_idx[identity]: []}
    queue = [elem_to_idx[identity]]
    while queue:
        curr = queue.pop(0)
        for i, g_idx in enumerate(gen_indices):
            nxt = mult_table[curr][g_idx]
            if nxt not in words:
                words[nxt] = words[curr] + [i]
                queue.append(nxt)
                
    aut_perms = []
    for prod in itertools.product(*candidates):
        mapping = {}
        for i in range(n):
            val = elem_to_idx[identity]
            for gen_idx in words[i]:
                val = mult_table[val][prod[gen_idx]]
            mapping[i] = val
            
        # Must be bijective
        if len(set(mapping.values())) != n:
            continue
            
        # Must preserve multiplication table
        is_hom = True
        for i in range(n):
            for j in range(n):
                if mapping[mult_table[i][j]] != mult_table[mapping[i]][mapping[j]]:
                    is_hom = False
                    break
            if not is_hom:
                break
                
        if is_hom:
            perm = [mapping[i] for i in range(n)]
            aut_perms.append(Permutation(perm))
            
    if not aut_perms:
        aut_perms.append(Permutation([i for i in range(n)]))
        
    AutG = PermutationGroup(aut_perms)
    return InnG, AutG, n

def conditions(witness):
    try:
        # H_1: G is a finite group
        if not isinstance(witness, PermutationGroup):
            return [False, False, False, False]
        if witness.order() < 1:
            return [False, False, False, False]
        h1 = True
    except Exception:
        return [False, False, False, False]
        
    try:
        # H_2 & H_3: Aut(G) and Inn(G) are well-defined
        InnG, AutG, n = get_aut_and_inn(witness)
        h2 = True
        h3 = True
    except Exception:
        return [h1, False, False, False]
        
    try:
        # ¬Q: Inn(G) is NOT a subgroup of the derived subgroup of Aut(G)
        try:
            AutG_derived = AutG.derived_subgroup()
        except AttributeError:
            # Fallback if derived_subgroup() is unavailable
            aut_elements = list(AutG.generate())
            commutators = []
            for x in aut_elements:
                for y in aut_elements:
                    commutators.append((~x) * (~y) * x * y)
            if commutators:
                AutG_derived = PermutationGroup(commutators)
            else:
                AutG_derived = PermutationGroup([Permutation([i for i in range(n)])])
                
        is_subgroup = True
        for g in InnG.generators:
            if g not in AutG_derived:
                is_subgroup = False
                break
        neg_q = not is_subgroup
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Aut(G) is the automorphism group of G",
    "H_3: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Inn(G) is not a subgroup of the derived subgroup of Aut(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3