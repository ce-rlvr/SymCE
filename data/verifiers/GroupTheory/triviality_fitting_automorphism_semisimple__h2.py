import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import factorint
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_generators(G):
    val = G.generators
    if callable(val):
        return val()
    return val

def get_automorphism_group(G):
    elts = list(G.generate())
    n = len(elts)
    if n == 1:
        return PermutationGroup([Permutation([0])])
        
    elt_to_idx = {e: i for i, e in enumerate(elts)}
    
    mult_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elt_to_idx[elts[i] * elts[j]]
            
    gens = get_generators(G)
    gen_indices = [elt_to_idx[g] for g in gens]
    
    identity = next(e for e in elts if e * e == e)
    id_idx = elt_to_idx[identity]
    
    def build_homomorphism(gen_mapping):
        mapping = {id_idx: id_idx}
        queue = [id_idx]
        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            for g_idx in gen_indices:
                nxt = mult_table[curr][g_idx]
                nxt_val = mult_table[mapping[curr]][gen_mapping[g_idx]]
                if nxt in mapping:
                    if mapping[nxt] != nxt_val:
                        return None
                else:
                    mapping[nxt] = nxt_val
                    queue.append(nxt)
        if len(mapping) == n:
            return mapping
        return None

    orders = [g.order() for g in gens]
    valid_targets = []
    for o in orders:
        valid_targets.append([i for i, e in enumerate(elts) if e.order() == o])
        
    automorphisms = []
    for target_tuple in itertools.product(*valid_targets):
        gen_mapping = {gen_indices[i]: target_tuple[i] for i in range(len(gens))}
        mapping = build_homomorphism(gen_mapping)
        if mapping is not None:
            if len(set(mapping.values())) == n:
                perm_array = [mapping[i] for i in range(n)]
                automorphisms.append(Permutation(perm_array))
                
    if not automorphisms:
        return PermutationGroup([Permutation([i for i in range(n)])])
    return PermutationGroup(automorphisms)

def get_conjugacy_classes(G_elts):
    classes = []
    unseen = set(G_elts)
    while unseen:
        x = unseen.pop()
        c = set()
        for g in G_elts:
            g_inv = ~g
            c.add(g * x * g_inv)
        classes.append(c)
        unseen -= c
    return classes

def generate_subgroup(subset, G_elts):
    subgroup = set(subset)
    identity = next(e for e in G_elts if e * e == e)
    subgroup.add(identity)
    
    subset_with_inv = set(subset)
    for s in subset:
        subset_with_inv.add(~s)
        
    queue = list(subgroup)
    head = 0
    while head < len(queue):
        curr = queue[head]
        head += 1
        for s in subset_with_inv:
            nxt = curr * s
            if nxt not in subgroup:
                subgroup.add(nxt)
                queue.append(nxt)
    return subgroup

def is_fitting_subgroup_trivial(AutG):
    AutG_elts = list(AutG.generate())
    if len(AutG_elts) == 1:
        return True
        
    classes = get_conjugacy_classes(AutG_elts)
    identity = next(e for e in AutG_elts if e * e == e)
    
    for c in classes:
        if c == {identity}:
            continue
            
        N_C = generate_subgroup(c, AutG_elts)
        
        n = len(N_C)
        if n > 1:
            factors = factorint(n)
            if len(factors) == 1:
                return False
                
    return True

def conditions(witness):
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: Aut(G) is the automorphism group of G
    h2 = h1
    
    # neg_Q: The Fitting subgroup of Aut(G) is not the trivial subgroup
    neg_q = False
    if h1:
        try:
            AutG = get_automorphism_group(witness)
            is_trivial = is_fitting_subgroup_trivial(AutG)
            neg_q = not is_trivial
        except Exception:
            neg_q = False
            
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Aut(G) is the automorphism group of G",
    "¬Q: The Fitting subgroup of Aut(G) is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2