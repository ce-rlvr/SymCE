import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_automorphisms(G):
    try:
        elements = list(G.elements)
    except Exception:
        elements = list(G.generate())
        
    # Sort elements to ensure determinism
    elements.sort(key=lambda x: str(x))
    
    n = len(elements)
    idx = {g: i for i, g in enumerate(elements)}
    mul_table = [[idx[g*h] for h in elements] for g in elements]
    
    id_idx = None
    for i in range(n):
        if all(mul_table[i][j] == j for j in range(n)):
            id_idx = i
            break
            
    inv = [0] * n
    for i in range(n):
        for j in range(n):
            if mul_table[i][j] == id_idx:
                inv[i] = j
                break

    conj_of = []
    for i in range(n):
        conjs = set()
        for g in range(n):
            gi = mul_table[g][i]
            gig_inv = mul_table[gi][inv[g]]
            conjs.add(gig_inv)
        conj_of.append(conjs)
        
    orders = [0] * n
    for i in range(n):
        curr = i
        order = 1
        while curr != id_idx:
            curr = mul_table[curr][i]
            order += 1
        orders[i] = order
        
    gens = list(G.generators)
    gens.sort(key=lambda x: str(x))
    gen_idx = [idx[g] for g in gens]
    
    possible_images = []
    for g in gen_idx:
        req_order = orders[g]
        req_conj_size = len(conj_of[g])
        possible_images.append([
            i for i in range(n) 
            if orders[i] == req_order and len(conj_of[i]) == req_conj_size
        ])
        
    auts = []
    
    for images in itertools.product(*possible_images):
        mapping = {gen_idx[i]: images[i] for i in range(len(gen_idx))}
        if id_idx in mapping and mapping[id_idx] != id_idx:
            continue
        mapping[id_idx] = id_idx
        
        queue = list(mapping.keys())
        head = 0
        conflict = False
        while head < len(queue):
            u = queue[head]
            head += 1
            for v in gen_idx:
                uv = mul_table[u][v]
                muv = mul_table[mapping[u]][mapping[v]]
                if uv in mapping:
                    if mapping[uv] != muv:
                        conflict = True
                        break
                else:
                    mapping[uv] = muv
                    queue.append(uv)
            if conflict:
                break
                
        if conflict or len(mapping) != n:
            continue
            
        if len(set(mapping.values())) != n:
            continue
            
        valid = True
        for i in range(n):
            for j in range(n):
                if mapping[mul_table[i][j]] != mul_table[mapping[i]][mapping[j]]:
                    valid = False
                    break
            if not valid:
                break
                
        if valid:
            aut = tuple(mapping[i] for i in range(n))
            auts.append(aut)
            
    return auts, elements, idx, mul_table, conj_of

def is_class_preserving(aut, conj_of, n):
    for i in range(n):
        if aut[i] not in conj_of[i]:
            return False
    return True

def compose(aut1, aut2, n):
    return tuple(aut1[aut2[i]] for i in range(n))

def is_normal_subgroup(N_auts, G_auts, n):
    N_set = set(N_auts)
    if not N_set:
        return False
    
    for n1 in N_auts:
        for n2 in N_auts:
            if compose(n1, n2, n) not in N_set:
                return False
                
    for n1 in N_auts:
        inv = [0]*n
        for i in range(n):
            inv[n1[i]] = i
        if tuple(inv) not in N_set:
            return False

    for n1 in N_auts:
        for g in G_auts:
            g_inv = [0]*n
            for i in range(n):
                g_inv[g[i]] = i
            g_inv = tuple(g_inv)
            
            conj = compose(g, compose(n1, g_inv, n), n)
            if conj not in N_set:
                return False
                
    return True

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            return [False, False]
            
        auts, elements, idx, mul_table, conj_of = get_automorphisms(witness)
        n = len(elements)
        
        aut_c = [aut for aut in auts if is_class_preserving(aut, conj_of, n)]
        
        is_normal = is_normal_subgroup(aut_c, auts, n)
        neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: Aut_c(G) is not a normal subgroup of Aut(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1