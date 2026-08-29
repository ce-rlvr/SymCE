import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def build_cayley(G, elements):
    n = len(elements)
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult[i][j] = elem_to_idx[elements[i] * elements[j]]
    return mult

def is_group(mult):
    n = len(mult)
    if n == 0: return False
    for row in mult:
        if len(row) != n: return False
        for x in row:
            if not isinstance(x, int) or not (0 <= x < n): return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mult[mult[i][j]][k] != mult[i][mult[j][k]]:
                    return False
    has_id = False
    for e in range(n):
        is_id = True
        for i in range(n):
            if mult[e][i] != i or mult[i][e] != i:
                is_id = False
                break
        if is_id:
            has_id = True
            break
    if not has_id: return False
    for i in range(n):
        has_inv = False
        for j in range(n):
            if mult[i][j] == e and mult[j][i] == e:
                has_inv = True
                break
        if not has_inv: return False
    return True

def is_valid_action(N_mult, H_mult, phi):
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
    id_H = None
    for e in range(n_H):
        if all(H_mult[e][i] == i for i in range(n_H)):
            id_H = e
            break
    if id_H is None: return False
    for n in range(n_N):
        if phi[id_H][n] != n:
            return False
    return True

def get_Z_G(N_mult, H_mult, phi):
    n_N = len(N_mult)
    n_H = len(H_mult)
    Z_G = []
    for n in range(n_N):
        for h in range(n_H):
            is_center = True
            for n1 in range(n_N):
                for h1 in range(n_H):
                    left_n = N_mult[n][phi[h][n1]]
                    left_h = H_mult[h][h1]
                    right_n = N_mult[n1][phi[h1][n]]
                    right_h = H_mult[h1][h]
                    if left_n != right_n or left_h != right_h:
                        is_center = False
                        break
                if not is_center:
                    break
            if is_center:
                Z_G.append((n, h))
    return Z_G

def get_A_B(N_mult, H_mult, phi):
    n_N = len(N_mult)
    n_H = len(H_mult)
    
    Z_N = [n for n in range(n_N) if all(N_mult[n][n1] == N_mult[n1][n] for n1 in range(n_N))]
    C_N_H = [n for n in range(n_N) if all(phi[h][n] == n for h in range(n_H))]
    A = set(Z_N).intersection(C_N_H)
    
    Z_H = [h for h in range(n_H) if all(H_mult[h][h1] == H_mult[h1][h] for h1 in range(n_H))]
    ker_phi = [h for h in range(n_H) if all(phi[h][n] == n for n in range(n_N))]
    B = set(Z_H).intersection(ker_phi)
    
    return A, B

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            if isinstance(witness[0], list) and len(witness[0]) > 0 and isinstance(witness[0][0], list):
                N_mult, H_mult, phi_table = witness
            else:
                N, H, phi = witness
                N_elems = list(N.generate()) if hasattr(N, 'generate') else list(N)
                H_elems = list(H.generate()) if hasattr(H, 'generate') else list(H)
                N_mult = build_cayley(N, N_elems)
                H_mult = build_cayley(H, H_elems)
                
                n_H = len(H_elems)
                n_N = len(N_elems)
                N_elem_to_idx = {e: i for i, e in enumerate(N_elems)}
                phi_table = [[0] * n_N for _ in range(n_H)]
                for i, h in enumerate(H_elems):
                    for j, n in enumerate(N_elems):
                        res = None
                        try:
                            res = phi(h, n)
                        except Exception:
                            try:
                                res = phi(h)(n)
                            except Exception:
                                try:
                                    res = phi[h][n]
                                except Exception:
                                    try:
                                        res = phi(h)[n]
                                    except Exception:
                                        pass
                        if res is None:
                            return [False, False, False]
                        phi_table[i][j] = N_elem_to_idx[res]
        else:
            return [False, False, False]
            
        h1 = is_group(N_mult) and is_group(H_mult) and is_valid_action(N_mult, H_mult, phi_table)
        h2 = h1
        
        if not h1:
            neg_q = False
        else:
            Z_G = get_Z_G(N_mult, H_mult, phi_table)
            A, B = get_A_B(N_mult, H_mult, phi_table)
            # A x B is always a subgroup of Z(G), so they are isomorphic iff they have the same size
            neg_q = len(Z_G) != len(A) * len(B)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G = N ⋊_phi H is an external semidirect product via phi: H -> Aut(N)",
    "H_2: ker(phi) is the kernel of the action phi",
    "¬Q: Z(G) is not isomorphic to (Z(N) ∩ C_N(H)) × (Z(H) ∩ ker(phi))"
]
N_HYP = 2
NEG_Q_INDEX = 2