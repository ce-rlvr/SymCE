import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def extract_witness(witness):
    N_elts = N_mul = H_elts = H_mul = phi = None
    
    if isinstance(witness, dict):
        if 'N_elts' in witness:
            N_elts = list(witness['N_elts'])
            N_mul = witness['N_mul']
            H_elts = list(witness['H_elts'])
            H_mul = witness['H_mul']
            phi = witness['phi']
        elif 'N' in witness:
            N = witness['N']
            H = witness['H']
            phi = witness['phi']
            N_elts = list(N.elements) if hasattr(N, 'elements') else list(N)
            N_mul = N.mul if hasattr(N, 'mul') else (lambda a, b: a * b)
            H_elts = list(H.elements) if hasattr(H, 'elements') else list(H)
            H_mul = H.mul if hasattr(H, 'mul') else (lambda a, b: a * b)
    elif isinstance(witness, tuple):
        if len(witness) == 5:
            N_elts, N_mul, H_elts, H_mul, phi = witness
            N_elts = list(N_elts)
            H_elts = list(H_elts)
        elif len(witness) == 3:
            N, H, phi = witness
            N_elts = list(N.elements) if hasattr(N, 'elements') else list(N)
            N_mul = N.mul if hasattr(N, 'mul') else (lambda a, b: a * b)
            H_elts = list(H.elements) if hasattr(H, 'elements') else list(H)
            H_mul = H.mul if hasattr(H, 'mul') else (lambda a, b: a * b)
    else:
        if hasattr(witness, 'N_elts'):
            N_elts = list(witness.N_elts)
            N_mul = witness.N_mul
            H_elts = list(witness.H_elts)
            H_mul = witness.H_mul
            phi = witness.phi
        elif hasattr(witness, 'N'):
            N = witness.N
            H = witness.H
            phi = witness.phi
            N_elts = list(N.elements) if hasattr(N, 'elements') else list(N)
            N_mul = N.mul if hasattr(N, 'mul') else (lambda a, b: a * b)
            H_elts = list(H.elements) if hasattr(H, 'elements') else list(H)
            H_mul = H.mul if hasattr(H, 'mul') else (lambda a, b: a * b)

    if isinstance(phi, dict):
        phi_dict = phi
        phi_func = lambda h, n: phi_dict[(h, n)]
    else:
        phi_func = phi

    def safe_phi(h, n):
        try:
            return phi_func(h, n)
        except TypeError:
            return phi_func(h)(n)

    return N_elts, N_mul, H_elts, H_mul, safe_phi

def is_group(elts, mul):
    if not elts: return False
    n_elts = len(elts)
    
    mul_table = [[None] * n_elts for _ in range(n_elts)]
    for i in range(n_elts):
        for j in range(n_elts):
            try:
                res = mul(elts[i], elts[j])
            except Exception:
                return False
            try:
                idx = elts.index(res)
                mul_table[i][j] = idx
            except ValueError:
                return False
                
    for i in range(n_elts):
        for j in range(n_elts):
            ij = mul_table[i][j]
            for k in range(n_elts):
                if mul_table[ij][k] != mul_table[i][mul_table[j][k]]:
                    return False
                    
    identity_idx = None
    for i in range(n_elts):
        is_id = True
        for j in range(n_elts):
            if mul_table[i][j] != j or mul_table[j][i] != j:
                is_id = False
                break
        if is_id:
            identity_idx = i
            break
    if identity_idx is None:
        return False
        
    for i in range(n_elts):
        has_inv = False
        for j in range(n_elts):
            if mul_table[i][j] == identity_idx and mul_table[j][i] == identity_idx:
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def check_LHS(N_elts, N_mul, H_elts, H_mul, phi):
    SD_elts = [(n, h) for n in N_elts for h in H_elts]
    n_elts = len(SD_elts)
    
    mul_table = [[None] * n_elts for _ in range(n_elts)]
    for i in range(n_elts):
        for j in range(n_elts):
            a = SD_elts[i]
            b = SD_elts[j]
            try:
                res = (N_mul(a[0], phi(a[1], b[0])), H_mul(a[1], b[1]))
            except Exception:
                return False
            try:
                idx = SD_elts.index(res)
                mul_table[i][j] = idx
            except ValueError:
                return False
                
    for i in range(n_elts):
        for j in range(n_elts):
            ij = mul_table[i][j]
            for k in range(n_elts):
                if mul_table[ij][k] != mul_table[i][mul_table[j][k]]:
                    return False
                    
    identity_idx = None
    for i in range(n_elts):
        is_id = True
        for j in range(n_elts):
            if mul_table[i][j] != j or mul_table[j][i] != j:
                is_id = False
                break
        if is_id:
            identity_idx = i
            break
    if identity_idx is None:
        return False
        
    for i in range(n_elts):
        has_inv = False
        for j in range(n_elts):
            if mul_table[i][j] == identity_idx and mul_table[j][i] == identity_idx:
                has_inv = True
                break
        if not has_inv:
            return False
            
    for i in range(n_elts):
        for j in range(n_elts):
            if mul_table[i][j] != mul_table[j][i]:
                return False
                
    return True

def check_RHS(N_elts, N_mul, H_elts, H_mul, phi):
    for a in N_elts:
        for b in N_elts:
            if N_mul(a, b) != N_mul(b, a):
                return False
    for a in H_elts:
        for b in H_elts:
            if H_mul(a, b) != H_mul(b, a):
                return False
    for h in H_elts:
        for n in N_elts:
            if phi(h, n) != n:
                return False
    return True

def conditions(witness):
    try:
        N_elts, N_mul, H_elts, H_mul, phi = extract_witness(witness)
    except Exception:
        return [False, False]

    try:
        h1_ok = is_group(N_elts, N_mul) and is_group(H_elts, H_mul)
    except Exception:
        h1_ok = False

    try:
        lhs = check_LHS(N_elts, N_mul, H_elts, H_mul, phi)
        rhs = check_RHS(N_elts, N_mul, H_elts, H_mul, phi)
        neg_q = not (lhs == rhs)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "¬Q: The semidirect product is an abelian group iff N, H are abelian and phi is trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1