import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup for witness expressions
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

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: G is the external semidirect product of N and H",
    "¬Q: N' is not a normal subgroup of G isomorphic to N"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_identity(op):
    n = len(op)
    for i in range(n):
        if all(op[i][j] == j for j in range(n)) and all(op[j][i] == j for j in range(n)):
            return i
    return -1

def is_group(op):
    n = len(op)
    if n == 0: return False
    for row in op:
        if len(row) != n: return False
        for x in row:
            if not (isinstance(x, int) and 0 <= x < n): return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if op[op[i][j]][k] != op[i][op[j][k]]:
                    return False
    e = get_identity(op)
    if e == -1: return False
    for i in range(n):
        has_inv = False
        for j in range(n):
            if op[i][j] == e and op[j][i] == e:
                has_inv = True
                break
        if not has_inv: return False
    return True

def get_cayley_table(G):
    if isinstance(G, list) and all(isinstance(row, list) for row in G):
        return G
    if hasattr(G, 'elements'):
        elems = list(G.elements)
        n = len(elems)
        op = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                prod = elems[i] * elems[j]
                if prod in elems:
                    op[i][j] = elems.index(prod)
                else:
                    return None
        return op
    return None

def get_G_op(N_op, H_op, phi):
    lenN = len(N_op)
    lenH = len(H_op)
    G_op = []
    for i in range(lenN * lenH):
        n1 = i // lenH
        h1 = i % lenH
        row = []
        for j in range(lenN * lenH):
            n2 = j // lenH
            h2 = j % lenH
            
            n_res = N_op[n1][phi[h1][n2]]
            h_res = H_op[h1][h2]
            row.append(n_res * lenH + h_res)
        G_op.append(row)
    return G_op

def check_conclusion(N_op, H_op, G_op):
    lenN = len(N_op)
    lenH = len(H_op)
    e_H = get_identity(H_op)
    e_G = get_identity(G_op)
    
    N_prime = [n * lenH + e_H for n in range(lenN)]
    
    # Check if N_prime is a subgroup
    if e_G not in N_prime:
        return False
        
    for x in N_prime:
        for y in N_prime:
            if G_op[x][y] not in N_prime:
                return False
                
    for x in N_prime:
        inv_x = -1
        for y in range(lenN * lenH):
            if G_op[x][y] == e_G and G_op[y][x] == e_G:
                inv_x = y
                break
        if inv_x not in N_prime:
            return False
            
    # Check if normal
    for x in N_prime:
        for g in range(lenN * lenH):
            g_inv = -1
            for y in range(lenN * lenH):
                if G_op[g][y] == e_G and G_op[y][g] == e_G:
                    g_inv = y
                    break
            if g_inv == -1: return False
            
            conj = G_op[G_op[g][x]][g_inv]
            if conj not in N_prime:
                return False
                
    # Check if isomorphic to N
    e_N = get_identity(N_op)
    N_prime_e = e_G
    
    N_prime_non_e = [x for x in N_prime if x != N_prime_e]
    N_non_e = [x for x in range(lenN) if x != e_N]
    
    for p_non_e in itertools.permutations(N_prime_non_e):
        p = [0] * lenN
        p[e_N] = N_prime_e
        for i, val in enumerate(N_non_e):
            p[val] = p_non_e[i]
            
        is_iso = True
        for i in range(lenN):
            for j in range(lenN):
                if G_op[p[i]][p[j]] != p[N_op[i][j]]:
                    is_iso = False
                    break
            if not is_iso:
                break
        if is_iso:
            return True
            
    return False

def conditions(witness):
    try:
        N, H, phi = witness
        
        N_op = get_cayley_table(N)
        H_op = get_cayley_table(H)
        
        if N_op is None or H_op is None:
            return [False, False, False]
            
        h1 = is_group(N_op) and is_group(H_op)
        if not h1:
            return [False, False, False]
            
        lenN = len(N_op)
        lenH = len(H_op)
        
        phi_table = []
        if isinstance(phi, list) and len(phi) == lenH and all(isinstance(row, list) for row in phi):
            phi_table = phi
        else:
            N_elems = list(N.elements) if hasattr(N, 'elements') else list(range(lenN))
            H_elems = list(H.elements) if hasattr(H, 'elements') else list(range(lenH))
            
            for i in range(lenH):
                row = []
                for j in range(lenN):
                    h = H_elems[i]
                    n = N_elems[j]
                    res = None
                    try:
                        res = phi(h, n)
                    except Exception:
                        try:
                            res = phi(h)(n)
                        except Exception:
                            try:
                                res = phi[h](n)
                            except Exception:
                                try:
                                    res = phi[h][n]
                                except Exception:
                                    pass
                    
                    if res in N_elems:
                        row.append(N_elems.index(res))
                    else:
                        break
                if len(row) != lenN:
                    break
                phi_table.append(row)
                
        h2 = False
        if len(phi_table) == lenH and all(len(row) == lenN for row in phi_table):
            if all(isinstance(x, int) and 0 <= x < lenN for row in phi_table for x in row):
                h2 = True
                
        if not (h1 and h2):
            return [h1, h2, False]
            
        G_op = get_G_op(N_op, H_op, phi_table)
        
        if not is_group(G_op):
            neg_q = True
        else:
            neg_q = not check_conclusion(N_op, H_op, G_op)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]