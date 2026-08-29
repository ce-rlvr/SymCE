import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_valid_group(mul):
    n = len(mul)
    if n == 0: return False
    for row in mul:
        if len(row) != n: return False
        for x in row:
            if not (0 <= x < n): return False
            
    id_elem = -1
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)) and all(mul[j][i] == j for j in range(n)):
            id_elem = i
            break
    if id_elem == -1: return False
    
    for i in range(n):
        has_inv = False
        for j in range(n):
            if mul[i][j] == id_elem and mul[j][i] == id_elem:
                has_inv = True
                break
        if not has_inv: return False
        
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]:
                    return False
    return True

def get_orders(mul_table, identity):
    n = len(mul_table)
    orders = []
    for i in range(n):
        curr = i
        order = 1
        while curr != identity and order <= n:
            curr = mul_table[curr][i]
            order += 1
        if order > n: return None
        orders.append(order)
    return orders

def are_isomorphic(mul1, mul2):
    n = len(mul1)
    if len(mul2) != n: return False
    
    def find_id(mul):
        for i in range(n):
            if all(mul[i][j] == j for j in range(n)) and all(mul[j][i] == j for j in range(n)):
                return i
        return -1
        
    id1 = find_id(mul1)
    id2 = find_id(mul2)
    if id1 == -1 or id2 == -1: return False
    
    orders1 = get_orders(mul1, id1)
    orders2 = get_orders(mul2, id2)
    if orders1 is None or orders2 is None: return False
    
    if sorted(orders1) != sorted(orders2):
        return False
        
    from collections import defaultdict
    cands = defaultdict(list)
    for i, o in enumerate(orders2):
        cands[o].append(i)
        
    mapping = {}
    used = set()
    
    def solve(idx):
        if idx == n:
            return True
        o = orders1[idx]
        for cand in cands[o]:
            if cand in used:
                continue
                
            mapping[idx] = cand
            ok = True
            
            for i in range(idx + 1):
                k = mul1[i][idx]
                if k <= idx:
                    if mul2[mapping[i]][cand] != mapping[k]:
                        ok = False; break
            
            if ok:
                for j in range(idx + 1):
                    k = mul1[idx][j]
                    if k <= idx:
                        if mul2[cand][mapping[j]] != mapping[k]:
                            ok = False; break
                            
            if ok:
                for i in range(idx):
                    for j in range(idx):
                        if mul1[i][j] == idx:
                            if mul2[mapping[i]][mapping[j]] != cand:
                                ok = False; break
                        if not ok: break
                        
            if ok:
                used.add(cand)
                if solve(idx + 1):
                    return True
                used.remove(cand)
                
            del mapping[idx]
            
        return False

    return solve(0)

def get_elems(G):
    if hasattr(G, 'generate'): return list(G.generate())
    if hasattr(G, 'elements'): return list(G.elements)
    return list(G)

def eval_map(f, x):
    if isinstance(f, dict): return f[x]
    if isinstance(f, list): return f[x]
    return f(x)

def check_h1_int(witness):
    N_mul = witness['N_mul']
    H_mul = witness['H_mul']
    phi = witness['phi']
    psi = witness['psi']
    
    if not is_valid_group(N_mul): return False
    if not is_valid_group(H_mul): return False
    
    n = len(N_mul)
    m = len(H_mul)
    
    if len(phi) != m or len(psi) != m: return False
    
    for h in range(m):
        if len(phi[h]) != n or len(psi[h]) != n: return False
        if sorted(phi[h]) != list(range(n)): return False
        if sorted(psi[h]) != list(range(n)): return False
        
        for i in range(n):
            for j in range(n):
                if phi[h][N_mul[i][j]] != N_mul[phi[h][i]][phi[h][j]]: return False
                if psi[h][N_mul[i][j]] != N_mul[psi[h][i]][psi[h][j]]: return False
                
    for h1 in range(m):
        for h2 in range(m):
            h3 = H_mul[h1][h2]
            for i in range(n):
                if phi[h3][i] != phi[h1][phi[h2][i]]: return False
                if psi[h3][i] != psi[h1][psi[h2][i]]: return False
                
    return True

def check_h2_int(witness):
    N_mul = witness['N_mul']
    H_mul = witness['H_mul']
    phi = witness['phi']
    psi = witness['psi']
    alpha = witness['alpha']
    
    n = len(N_mul)
    m = len(H_mul)
    
    if len(alpha) != n: return False
    if sorted(alpha) != list(range(n)): return False
    
    for i in range(n):
        for j in range(n):
            if alpha[N_mul[i][j]] != N_mul[alpha[i]][alpha[j]]: return False
            
    for h in range(m):
        for i in range(n):
            if psi[h][alpha[i]] != alpha[phi[h][i]]: return False
            
    return True

def check_neg_q_int(witness):
    N_mul = witness['N_mul']
    H_mul = witness['H_mul']
    phi = witness['phi']
    psi = witness['psi']
    
    n = len(N_mul)
    m = len(H_mul)
    
    G1_mul = [[0] * (n * m) for _ in range(n * m)]
    G2_mul = [[0] * (n * m) for _ in range(n * m)]
    
    for n1 in range(n):
        for h1 in range(m):
            idx1 = n1 * m + h1
            for n2 in range(n):
                for h2 in range(m):
                    idx2 = n2 * m + h2
                    
                    p_n_G1 = N_mul[n1][phi[h1][n2]]
                    p_h_G1 = H_mul[h1][h2]
                    G1_mul[idx1][idx2] = p_n_G1 * m + p_h_G1
                    
                    p_n_G2 = N_mul[n1][psi[h1][n2]]
                    p_h_G2 = H_mul[h1][h2]
                    G2_mul[idx1][idx2] = p_n_G2 * m + p_h_G2
                    
    return not are_isomorphic(G1_mul, G2_mul)

def check_h1_sympy(witness):
    N = witness['N']
    H = witness['H']
    phi = witness['phi']
    psi = witness['psi']
    
    N_elems = get_elems(N)
    H_elems = get_elems(H)
    
    for h in H_elems:
        phi_h = eval_map(phi, h)
        psi_h = eval_map(psi, h)
        
        phi_h_img = [eval_map(phi_h, n) for n in N_elems]
        psi_h_img = [eval_map(psi_h, n) for n in N_elems]
        
        if len(set(phi_h_img)) != len(N_elems): return False
        if len(set(psi_h_img)) != len(N_elems): return False
        for img in phi_h_img:
            if img not in N_elems: return False
        for img in psi_h_img:
            if img not in N_elems: return False
            
        for n1 in N_elems:
            for n2 in N_elems:
                if eval_map(phi_h, n1 * n2) != eval_map(phi_h, n1) * eval_map(phi_h, n2): return False
                if eval_map(psi_h, n1 * n2) != eval_map(psi_h, n1) * eval_map(psi_h, n2): return False
                
    for h1 in H_elems:
        for h2 in H_elems:
            h3 = h1 * h2
            phi_h1 = eval_map(phi, h1)
            phi_h2 = eval_map(phi, h2)
            phi_h3 = eval_map(phi, h3)
            
            psi_h1 = eval_map(psi, h1)
            psi_h2 = eval_map(psi, h2)
            psi_h3 = eval_map(psi, h3)
            
            for n in N_elems:
                if eval_map(phi_h3, n) != eval_map(phi_h1, eval_map(phi_h2, n)): return False
                if eval_map(psi_h3, n) != eval_map(psi_h1, eval_map(psi_h2, n)): return False
                
    return True

def check_h2_sympy(witness):
    N = witness['N']
    H = witness['H']
    phi = witness['phi']
    psi = witness['psi']
    alpha = witness['alpha']
    
    N_elems = get_elems(N)
    H_elems = get_elems(H)
    
    alpha_img = [eval_map(alpha, n) for n in N_elems]
    if len(set(alpha_img)) != len(N_elems): return False
    for img in alpha_img:
        if img not in N_elems: return False
        
    for n1 in N_elems:
        for n2 in N_elems:
            if eval_map(alpha, n1 * n2) != eval_map(alpha, n1) * eval_map(alpha, n2): return False
            
    for h in H_elems:
        phi_h = eval_map(phi, h)
        psi_h = eval_map(psi, h)
        for n in N_elems:
            left = eval_map(psi_h, eval_map(alpha, n))
            right = eval_map(alpha, eval_map(phi_h, n))
            if left != right: return False
            
    return True

def check_neg_q_sympy(witness):
    N = witness['N']
    H = witness['H']
    phi = witness['phi']
    psi = witness['psi']
    
    N_elems = get_elems(N)
    H_elems = get_elems(H)
    
    n_len = len(N_elems)
    m_len = len(H_elems)
    
    G1_mul = [[0] * (n_len * m_len) for _ in range(n_len * m_len)]
    G2_mul = [[0] * (n_len * m_len) for _ in range(n_len * m_len)]
    
    for i1, n1 in enumerate(N_elems):
        for j1, h1 in enumerate(H_elems):
            idx1 = i1 * m_len + j1
            
            phi_h1 = eval_map(phi, h1)
            psi_h1 = eval_map(psi, h1)
            
            for i2, n2 in enumerate(N_elems):
                for j2, h2 in enumerate(H_elems):
                    idx2 = i2 * m_len + j2
                    
                    p_n_G1 = n1 * eval_map(phi_h1, n2)
                    p_h_G1 = h1 * h2
                    
                    idx_n_G1 = N_elems.index(p_n_G1)
                    idx_h_G1 = H_elems.index(p_h_G1)
                    G1_mul[idx1][idx2] = idx_n_G1 * m_len + idx_h_G1
                    
                    p_n_G2 = n1 * eval_map(psi_h1, n2)
                    p_h_G2 = h1 * h2
                    
                    idx_n_G2 = N_elems.index(p_n_G2)
                    idx_h_G2 = H_elems.index(p_h_G2)
                    G2_mul[idx1][idx2] = idx_n_G2 * m_len + idx_h_G2
                    
    return not are_isomorphic(G1_mul, G2_mul)

def check_h1(witness):
    if not isinstance(witness, dict): return False
    if 'N_mul' in witness: return check_h1_int(witness)
    return check_h1_sympy(witness)

def check_h2(witness):
    if not isinstance(witness, dict): return False
    if 'N_mul' in witness: return check_h2_int(witness)
    return check_h2_sympy(witness)

def check_neg_q(witness):
    if not isinstance(witness, dict): return False
    if 'N_mul' in witness: return check_neg_q_int(witness)
    return check_neg_q_sympy(witness)

def conditions(witness):
    try:
        h1 = check_h1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_h2(witness)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_q(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi and psi are homomorphisms from H to Aut(N)",
    "H_2: psi is conjugate to phi by some alpha in Aut(N)",
    "¬Q: N rtimes_phi H and N rtimes_psi H are NOT isomorphic"
]
N_HYP = 2
NEG_Q_INDEX = 2