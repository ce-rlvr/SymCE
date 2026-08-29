import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(elems, op, identity):
    if not elems: return False
    if identity not in elems: return False
    for a in elems:
        try:
            if op(a, identity) != a or op(identity, a) != a: return False
        except Exception:
            return False
        has_inv = False
        for b in elems:
            try:
                if op(a, b) == identity and op(b, a) == identity:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv: return False
        for b in elems:
            try:
                ab = op(a, b)
            except Exception:
                return False
            if ab not in elems: return False
            for c in elems:
                try:
                    if op(ab, c) != op(a, op(b, c)): return False
                except Exception:
                    return False
    return True

def is_hom(A_elems, A_op, B_elems, B_op, func):
    for a in A_elems:
        try:
            fa = func(a)
        except Exception:
            return False
        if fa not in B_elems: return False
        for b in A_elems:
            try:
                if func(A_op(a, b)) != B_op(fa, func(b)): return False
            except Exception:
                return False
    return True

def get_inverse(K_elems, K_op, K_id, k):
    for k_inv in K_elems:
        try:
            if K_op(k, k_inv) == K_id and K_op(k_inv, k) == K_id:
                return k_inv
        except Exception:
            pass
    return None

def count_valid_homs(N_elems, N_id, H_elems, H_id, G_elems, G_op, K_elems, K_op, f, g):
    assignment = {}
    for n in N_elems:
        pair = (n, H_id)
        if pair not in G_elems: return 0
        try:
            assignment[pair] = f(n)
        except Exception:
            return 0
            
    for h in H_elems:
        pair = (N_id, h)
        if pair not in G_elems: return 0
        try:
            gh = g(h)
        except Exception:
            return 0
        if pair in assignment and assignment[pair] != gh:
            return 0
        assignment[pair] = gh
            
    G_list = list(G_elems)
    n_G = len(G_list)
    K_list = list(K_elems)
    
    G_idx = {x: i for i, x in enumerate(G_list)}
    K_idx = {x: i for i, x in enumerate(K_list)}
    
    try:
        G_op_idx = [[G_idx[G_op(x, y)] for y in G_list] for x in G_list]
        K_op_idx = [[K_idx[K_op(x, y)] for y in K_list] for x in K_list]
    except Exception:
        return 0
        
    pairs_yielding = [[] for _ in range(n_G)]
    for i in range(n_G):
        for j in range(n_G):
            pairs_yielding[G_op_idx[i][j]].append((i, j))
            
    mapping = [-1] * n_G
    for x, val in assignment.items():
        if val not in K_idx: return 0
        mapping[G_idx[x]] = K_idx[val]
        
    valid_count = [0]
    
    def is_consistent(idx):
        for i in range(n_G):
            if mapping[i] == -1: continue
            
            p1 = G_op_idx[i][idx]
            if mapping[p1] != -1:
                if mapping[p1] != K_op_idx[mapping[i]][mapping[idx]]: return False
                
            p2 = G_op_idx[idx][i]
            if mapping[p2] != -1:
                if mapping[p2] != K_op_idx[mapping[idx]][mapping[i]]: return False
                
        for i, j in pairs_yielding[idx]:
            if mapping[i] != -1 and mapping[j] != -1:
                if mapping[idx] != K_op_idx[mapping[i]][mapping[j]]: return False
                
        return True

    def search(idx):
        if valid_count[0] > 1:
            return
        if idx == n_G:
            valid_count[0] += 1
            return
            
        if mapping[idx] != -1:
            if is_consistent(idx):
                search(idx + 1)
            return
            
        for k in range(len(K_list)):
            mapping[idx] = k
            if is_consistent(idx):
                search(idx + 1)
        mapping[idx] = -1

    search(0)
    return valid_count[0]

def check_Q(N_elems, H_elems, K_elems, K_op, K_id, phi, f, g):
    for n in N_elems:
        for h in H_elems:
            try:
                try:
                    n_prime = phi(h, n)
                except Exception:
                    n_prime = phi(h)(n)
                if n_prime not in N_elems: return False
                left = f(n_prime)
                g_h = g(h)
                g_h_inv = get_inverse(K_elems, K_op, K_id, g_h)
                if g_h_inv is None: return False
                right = K_op(K_op(g_h, f(n)), g_h_inv)
                if left != right:
                    return False
            except Exception:
                return False
    return True

def conditions(witness):
    try:
        K = witness['K']
        K_elems, K_op, K_id = K
        h1 = is_group(K_elems, K_op, K_id)
    except Exception:
        h1 = False

    try:
        N = witness['N']
        H = witness['H']
        f = witness['f']
        g = witness['g']
        N_elems, N_op, N_id = N
        H_elems, H_op, H_id = H
        
        h2 = (is_group(N_elems, N_op, N_id) and 
              is_group(H_elems, H_op, H_id) and 
              is_hom(N_elems, N_op, K_elems, K_op, f) and 
              is_hom(H_elems, H_op, K_elems, K_op, g))
    except Exception:
        h2 = False

    try:
        G = witness['G']
        G_elems, G_op, G_id = G
        phi = witness['phi']
        
        if not is_group(G_elems, G_op, G_id):
            P = False
        else:
            count = count_valid_homs(N_elems, N_id, H_elems, H_id, G_elems, G_op, K_elems, K_op, f, g)
            P = (count == 1)
            
        Q = check_Q(N_elems, H_elems, K_elems, K_op, K_id, phi, f, g)
        
        neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a group",
    "H_2: f: N -> K and g: H -> K are group homomorphisms",
    "¬Q: The equivalence between the unique extension property and the compatibility condition fails"
]

N_HYP = 2
NEG_Q_INDEX = 2