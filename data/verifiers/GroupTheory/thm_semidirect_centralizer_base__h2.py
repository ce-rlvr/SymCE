import itertools
import functools
import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is the external semidirect product of N by H with respect to φ: H → Aut(N)",
    "H_2: C_G(N) is the centralizer of N in G",
    "¬Q: C_G(N) is not exactly Z(N) × ker(φ)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_group(mult):
    n = len(mult)
    if n == 0: return False
    for row in mult:
        if len(row) != n: return False
        for x in row:
            if not (0 <= x < n): return False
            
    id_elem = -1
    for i in range(n):
        is_id = True
        for j in range(n):
            if mult[i][j] != j or mult[j][i] != j:
                is_id = False
                break
        if is_id:
            id_elem = i
            break
            
    if id_elem == -1:
        return False
        
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mult[mult[i][j]][k] != mult[i][mult[j][k]]:
                    return False
                    
    for i in range(n):
        has_inv = False
        for j in range(n):
            if mult[i][j] == id_elem and mult[j][i] == id_elem:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def is_hom_to_aut(N_mult, H_mult, phi):
    n_N = len(N_mult)
    n_H = len(H_mult)
    if len(phi) != n_H: return False
    for h in range(n_H):
        if len(phi[h]) != n_N: return False
        if set(phi[h]) != set(range(n_N)): return False
        for n1 in range(n_N):
            for n2 in range(n_N):
                if phi[h][N_mult[n1][n2]] != N_mult[phi[h][n1]][phi[h][n2]]:
                    return False
    for h1 in range(n_H):
        for h2 in range(n_H):
            h12 = H_mult[h1][h2]
            for n in range(n_N):
                if phi[h12][n] != phi[h1][phi[h2][n]]:
                    return False
    return True

def parse_witness(witness):
    if isinstance(witness, dict) and 'N_mult' in witness:
        return witness['N_mult'], witness['H_mult'], witness['phi']
    
    N, H, phi_func = witness
    
    def get_elements(G):
        if hasattr(G, 'elements'):
            return list(G.elements)
        return list(G)
        
    def get_identity(G, elems):
        if hasattr(G, 'identity'):
            return G.identity
        for e in elems:
            is_id = True
            for x in elems:
                if e*x != x or x*e != x:
                    is_id = False
                    break
            if is_id: return e
        return elems[0]

    N_elems = get_elements(N)
    id_N = get_identity(N, N_elems)
    N_elems = [e for e in N_elems if e != id_N]
    N_elems.insert(0, id_N)
    
    H_elems = get_elements(H)
    id_H = get_identity(H, H_elems)
    H_elems = [e for e in H_elems if e != id_H]
    H_elems.insert(0, id_H)
    
    n_N = len(N_elems)
    N_mult = [[0]*n_N for _ in range(n_N)]
    for i, e1 in enumerate(N_elems):
        for j, e2 in enumerate(N_elems):
            prod = e1 * e2
            idx = -1
            for k, e in enumerate(N_elems):
                if e == prod:
                    idx = k
                    break
            if idx == -1:
                raise ValueError("N is not closed under multiplication")
            N_mult[i][j] = idx
            
    n_H = len(H_elems)
    H_mult = [[0]*n_H for _ in range(n_H)]
    for i, e1 in enumerate(H_elems):
        for j, e2 in enumerate(H_elems):
            prod = e1 * e2
            idx = -1
            for k, e in enumerate(H_elems):
                if e == prod:
                    idx = k
                    break
            if idx == -1:
                raise ValueError("H is not closed under multiplication")
            H_mult[i][j] = idx
            
    phi = []
    for h in H_elems:
        aut = phi_func(h) if callable(phi_func) else phi_func[h]
        phi_h = []
        for n in N_elems:
            mapped_n = aut(n) if callable(aut) else aut[n]
            idx = -1
            for k, e in enumerate(N_elems):
                if e == mapped_n:
                    idx = k
                    break
            if idx == -1:
                raise ValueError("phi(h)(n) not in N")
            phi_h.append(idx)
        phi.append(phi_h)
        
    return N_mult, H_mult, phi

def conditions(witness):
    try:
        N_mult, H_mult, phi = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_group(N_mult) and is_group(H_mult) and is_hom_to_aut(N_mult, H_mult, phi)
    except Exception:
        h1_ok = False
        
    try:
        # H2 is definitional. If H1 is ok, we can form G and compute C_G(N).
        h2_ok = h1_ok
    except Exception:
        h2_ok = False
        
    try:
        if not h1_ok:
            neg_q = False
        else:
            n_N = len(N_mult)
            n_H = len(H_mult)
            
            C_G_N = set()
            for n in range(n_N):
                for h in range(n_H):
                    commutes = True
                    for n_prime in range(n_N):
                        left_n = N_mult[n][phi[h][n_prime]]
                        right_n = N_mult[n_prime][n]
                        if left_n != right_n:
                            commutes = False
                            break
                    if commutes:
                        C_G_N.add((n, h))
                        
            Z_N = set()
            for n in range(n_N):
                is_central = True
                for n_prime in range(n_N):
                    if N_mult[n][n_prime] != N_mult[n_prime][n]:
                        is_central = False
                        break
                if is_central:
                    Z_N.add(n)
                    
            ker_phi = set()
            for h in range(n_H):
                is_id = True
                for n in range(n_N):
                    if phi[h][n] != n:
                        is_id = False
                        break
                if is_id:
                    ker_phi.add(h)
                    
            expected_C_G_N = set((n, h) for n in Z_N for h in ker_phi)
            
            neg_q = (C_G_N != expected_C_G_N)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]