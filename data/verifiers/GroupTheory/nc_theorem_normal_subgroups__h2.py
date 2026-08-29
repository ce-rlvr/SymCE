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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_automorphisms(N):
    elements = list(N.elements)
    n = len(elements)
    gens = N.generators
    
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
            
    auts = []
    for target in itertools.product(elements, repeat=len(gens)):
        mapping = {id_elem: id_elem}
        valid = True
        
        queue = [id_elem]
        head = 0
        while head < len(queue) and valid:
            curr = queue[head]
            head += 1
            for g, t in zip(gens, target):
                nxt = curr * g
                nxt_val = mapping[curr] * t
                if nxt in mapping:
                    if mapping[nxt] != nxt_val:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_val
                    queue.append(nxt)
                    
        if valid and len(mapping) == n and len(set(mapping.values())) == n:
            auts.append(mapping)
            
    return auts

def get_aut_mult_table(auts, N):
    elements = list(N.elements)
    aut_to_idx = {}
    for i, aut in enumerate(auts):
        tup = tuple(aut[e] for e in elements)
        aut_to_idx[tup] = i
        
    n = len(auts)
    mult = [[0] * n for _ in range(n)]
    for i, aut1 in enumerate(auts):
        for j, aut2 in enumerate(auts):
            tup = tuple(aut1[aut2[e]] for e in elements)
            mult[i][j] = aut_to_idx[tup]
    return mult

def get_q_generators(mult, id_idx):
    n = len(mult)
    elements = list(range(n))
    gens = []
    closure = {id_idx}
    for e in elements:
        if e not in closure:
            gens.append(e)
            queue = [id_idx]
            new_closure = {id_idx}
            q_head = 0
            while q_head < len(queue):
                curr = queue[q_head]
                q_head += 1
                for g in gens:
                    nxt = mult[curr][g]
                    if nxt not in new_closure:
                        new_closure.add(nxt)
                        queue.append(nxt)
            closure = new_closure
            if len(closure) == n:
                break
    return gens

def is_isomorphic_to_subgroup(q_mult, q_id, a_mult, a_id):
    n_q = len(q_mult)
    n_a = len(a_mult)
    if n_q > n_a:
        return False
    if n_q == 1:
        return True
    if n_a % n_q != 0:
        return False
        
    q_gens = get_q_generators(q_mult, q_id)
    
    for target in itertools.product(range(n_a), repeat=len(q_gens)):
        mapping = {q_id: a_id}
        valid = True
        
        queue = [q_id]
        head = 0
        while head < len(queue) and valid:
            q1 = queue[head]
            a1 = mapping[q1]
            head += 1
            for g, t in zip(q_gens, target):
                q_new = q_mult[q1][g]
                a_new = a_mult[a1][t]
                if q_new in mapping:
                    if mapping[q_new] != a_new:
                        valid = False
                        break
                else:
                    mapping[q_new] = a_new
                    queue.append(q_new)
                    
        if valid and len(mapping) == n_q:
            if len(set(mapping.values())) == n_q:
                full_valid = True
                for i in range(n_q):
                    for j in range(n_q):
                        if mapping[q_mult[i][j]] != a_mult[mapping[i]][mapping[j]]:
                            full_valid = False
                            break
                    if not full_valid:
                        break
                if full_valid:
                    return True
    return False

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(N, PermutationGroup) or not N.is_subgroup(G):
            neg_q = False
        else:
            c_elements = []
            n_elements = list(N.elements)
            for g in G.elements:
                if all(g * n * ~g == n for n in n_elements):
                    c_elements.append(g)
            C = PermutationGroup(c_elements)
            
            is_normal = True
            c_set = set(c_elements)
            for g in G.generators:
                for c in C.generators:
                    if g * c * ~g not in c_set:
                        is_normal = False
                        break
                    if ~g * c * g not in c_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
            if not is_normal:
                # If C_G(N) is not normal in G, the quotient G/C_G(N) is not a group,
                # hence it cannot be isomorphic to a subgroup of Aut(N).
                neg_q = True
            else:
                cosets = []
                seen = set()
                for g in G.elements:
                    if g not in seen:
                        coset = frozenset(g * c for c in c_elements)
                        cosets.append(coset)
                        seen.update(coset)
                
                id_coset = frozenset(c_elements)
                coset_idx = {c: i for i, c in enumerate(cosets)}
                
                n_q = len(cosets)
                q_mult = [[0] * n_q for _ in range(n_q)]
                for i, c1 in enumerate(cosets):
                    g1 = next(iter(c1))
                    for j, c2 in enumerate(cosets):
                        g2 = next(iter(c2))
                        g3 = g1 * g2
                        for k, c3 in enumerate(cosets):
                            if g3 in c3:
                                q_mult[i][j] = k
                                break
                q_id = coset_idx[id_coset]
                
                auts = get_automorphisms(N)
                a_mult = get_aut_mult_table(auts, N)
                
                a_id = 0
                for i, aut in enumerate(auts):
                    if all(aut[e] == e for e in n_elements):
                        a_id = i
                        break
                        
                is_iso = is_isomorphic_to_subgroup(q_mult, q_id, a_mult, a_id)
                neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The quotient group G/C_G(N) is not isomorphic to a subgroup of Aut(N)"
]

N_HYP = 1
NEG_Q_INDEX = 1