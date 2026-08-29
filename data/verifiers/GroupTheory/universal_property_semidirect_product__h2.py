import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(elems, mult):
    if not elems: return False
    for a in elems:
        for b in elems:
            try:
                if mult(a, b) not in elems:
                    return False
            except Exception:
                return False
    for a in elems:
        for b in elems:
            for c in elems:
                try:
                    if mult(mult(a, b), c) != mult(a, mult(b, c)):
                        return False
                except Exception:
                    return False
    id_elem = None
    for e in elems:
        try:
            if all(mult(e, a) == a and mult(a, e) == a for a in elems):
                id_elem = e
                break
        except Exception:
            pass
    if id_elem is None: return False
    for a in elems:
        has_inv = False
        for b in elems:
            try:
                if mult(a, b) == id_elem and mult(b, a) == id_elem:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv:
            return False
    return True

def get_identity(elems, mult):
    for e in elems:
        try:
            if all(mult(e, a) == a and mult(a, e) == a for a in elems):
                return e
        except Exception:
            pass
    return None

def count_homomorphisms(G_elems, G_mult, K_elems, K_mult, fixed_mappings):
    n_G = len(G_elems)
    n_K = len(K_elems)
    
    def get_idx(elems, val):
        for i, e in enumerate(elems):
            if e == val: return i
        return -1

    G_table = []
    for a in G_elems:
        row = []
        for b in G_elems:
            idx = get_idx(G_elems, G_mult(a, b))
            if idx == -1: return 0
            row.append(idx)
        G_table.append(row)
        
    K_table = []
    for a in K_elems:
        row = []
        for b in K_elems:
            idx = get_idx(K_elems, K_mult(a, b))
            if idx == -1: return 0
            row.append(idx)
        K_table.append(row)
        
    phi = [-1] * n_G
    for g, k in fixed_mappings:
        g_idx = get_idx(G_elems, g)
        k_idx = get_idx(K_elems, k)
        if g_idx != -1 and k_idx != -1:
            if phi[g_idx] != -1 and phi[g_idx] != k_idx:
                return 0
            phi[g_idx] = k_idx
        else:
            return 0
            
    for i in range(n_G):
        if phi[i] == -1: continue
        for j in range(n_G):
            if phi[j] == -1: continue
            ij = G_table[i][j]
            if phi[ij] != -1 and phi[ij] != K_table[phi[i]][phi[j]]:
                return 0

    inverse_G_table = [[] for _ in range(n_G)]
    for i in range(n_G):
        for j in range(n_G):
            inverse_G_table[G_table[i][j]].append((i, j))

    count = [0]
    
    def search(idx):
        if count[0] > 1: return
        if idx == n_G:
            count[0] += 1
            return
            
        if phi[idx] != -1:
            search(idx + 1)
            return
            
        for k in range(n_K):
            phi[idx] = k
            consistent = True
            
            for i in range(n_G):
                if phi[i] == -1: continue
                
                ij = G_table[i][idx]
                if phi[ij] != -1 and phi[ij] != K_table[phi[i]][k]:
                    consistent = False
                    break
                    
                ji = G_table[idx][i]
                if phi[ji] != -1 and phi[ji] != K_table[k][phi[i]]:
                    consistent = False
                    break
            
            if not consistent:
                phi[idx] = -1
                continue
                
            for i, j in inverse_G_table[idx]:
                if phi[i] != -1 and phi[j] != -1:
                    if k != K_table[phi[i]][phi[j]]:
                        consistent = False
                        break
                        
            if consistent:
                search(idx + 1)
                
            phi[idx] = -1

    search(0)
    return count[0]

def conditions(witness):
    try:
        N = witness['N']
        H = witness['H']
        K = witness['K']
        N_mult = witness['N_mult']
        H_mult = witness['H_mult']
        K_mult = witness['K_mult']
        phi = witness['phi']
        f = witness['f']
        g = witness['g']
        G_mult = witness['G_mult']
    except Exception:
        return [False] * 6

    try:
        h1_ok = False
        if is_group(N, N_mult) and is_group(H, H_mult):
            H_id = get_identity(H, H_mult)
            phi_ok = True
            for h in H:
                img = []
                for n in N:
                    res = phi(h, n)
                    if res not in img:
                        img.append(res)
                if len(img) != len(N) or any(x not in N for x in img):
                    phi_ok = False
                    break
                for n1 in N:
                    for n2 in N:
                        if phi(h, N_mult(n1, n2)) != N_mult(phi(h, n1), phi(h, n2)):
                            phi_ok = False
                            break
                    if not phi_ok: break
                if not phi_ok: break
            if phi_ok:
                for h1 in H:
                    for h2 in H:
                        h12 = H_mult(h1, h2)
                        for n in N:
                            if phi(h12, n) != phi(h1, phi(h2, n)):
                                phi_ok = False
                                break
                        if not phi_ok: break
                    if not phi_ok: break
            if phi_ok:
                for n in N:
                    if phi(H_id, n) != n:
                        phi_ok = False
                        break
            h1_ok = phi_ok
    except Exception:
        h1_ok = False

    try:
        h2_ok = is_group(K, K_mult)
    except Exception:
        h2_ok = False

    try:
        h3_ok = True
        for n1 in N:
            for n2 in N:
                if f(N_mult(n1, n2)) != K_mult(f(n1), f(n2)):
                    h3_ok = False
                    break
            if not h3_ok: break
        if h3_ok:
            for h1 in H:
                for h2 in H:
                    if g(H_mult(h1, h2)) != K_mult(g(h1), g(h2)):
                        h3_ok = False
                        break
                if not h3_ok: break
        if h3_ok:
            if any(f(n) not in K for n in N) or any(g(h) not in K for h in H):
                h3_ok = False
    except Exception:
        h3_ok = False

    try:
        h4_ok = True
        K_id = get_identity(K, K_mult)
        def K_inv(k):
            for x in K:
                if K_mult(k, x) == K_id and K_mult(x, k) == K_id:
                    return x
            return None
        f_N = []
        for n in N:
            fn = f(n)
            if fn not in f_N:
                f_N.append(fn)
        for h in H:
            gh = g(h)
            gh_inv = K_inv(gh)
            if gh_inv is None:
                h4_ok = False
                break
            for fn in f_N:
                conj = K_mult(K_mult(gh, fn), gh_inv)
                if conj not in f_N:
                    h4_ok = False
                    break
            if not h4_ok: break
    except Exception:
        h4_ok = False

    try:
        h5_ok = True
        K_id = get_identity(K, K_mult)
        def K_inv(k):
            for x in K:
                if K_mult(k, x) == K_id and K_mult(x, k) == K_id:
                    return x
            return None
        for h in H:
            gh = g(h)
            gh_inv = K_inv(gh)
            if gh_inv is None:
                h5_ok = False
                break
            for n in N:
                left = f(phi(h, n))
                right = K_mult(K_mult(gh, f(n)), gh_inv)
                if left != right:
                    h5_ok = False
                    break
            if not h5_ok: break
    except Exception:
        h5_ok = False

    try:
        N_id = get_identity(N, N_mult)
        H_id = get_identity(H, H_mult)
        G_elems = []
        for n in N:
            for h in H:
                if (n, h) not in G_elems:
                    G_elems.append((n, h))
        
        if not is_group(G_elems, G_mult):
            neg_q_ok = True
        else:
            fixed_mappings = []
            for n in N:
                fixed_mappings.append(((n, H_id), f(n)))
            for h in H:
                fixed_mappings.append(((N_id, h), g(h)))
                
            count = count_homomorphisms(G_elems, G_mult, K, K_mult, fixed_mappings)
            neg_q_ok = (count != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, h5_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N and H are groups and phi: H -> Aut(N) is a homomorphism",
    "H_2: K is a group",
    "H_3: f: N -> K and g: H -> K are group homomorphisms",
    "H_4: f(N) is normalized by g(H) in K",
    "H_5: f(phi_h(n)) = g(h) f(n) g(h)^-1 for all n in N and h in H",
    "¬Q: There does not exist a unique group homomorphism Phi: G -> K such that Phi((n, 1_H)) = f(n) and Phi((1_N, h)) = g(h)"
]

N_HYP = 5
NEG_Q_INDEX = 5