import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def apply_phi(phi, h, n):
    if callable(phi):
        try:
            return phi(h, n)
        except TypeError:
            return phi(h)(n)
    elif isinstance(phi, dict):
        return phi[h][n]
    else:
        return phi[h][n]

def parse_witness(witness):
    if isinstance(witness, dict):
        N = witness.get('N')
        H = witness.get('H')
        phi = witness.get('phi')
        op_N = witness.get('op_N', lambda x, y: x * y)
        op_H = witness.get('op_H', lambda x, y: x * y)
    elif isinstance(witness, tuple):
        N = witness[0]
        H = witness[1]
        phi = witness[2]
        op_N = witness[3] if len(witness) > 3 else lambda x, y: x * y
        op_H = witness[4] if len(witness) > 4 else lambda x, y: x * y
    else:
        N = witness.N
        H = witness.H
        phi = witness.phi
        op_N = getattr(witness, 'op_N', lambda x, y: x * y)
        op_H = getattr(witness, 'op_H', lambda x, y: x * y)
        
    N_elems = get_elements(N)
    H_elems = get_elements(H)
    
    return N_elems, H_elems, phi, op_N, op_H

def find_identity(elems, op):
    for e in elems:
        if all(op(e, x) == x and op(x, e) == x for x in elems):
            return e
    return None

def is_group(elems, op):
    if not elems: return False
    for a in elems:
        for b in elems:
            if op(a, b) not in elems: return False
    for a in elems:
        for b in elems:
            for c in elems:
                if op(op(a, b), c) != op(a, op(b, c)): return False
    id_elem = find_identity(elems, op)
    if id_elem is None: return False
    for a in elems:
        has_inv = False
        for b in elems:
            if op(a, b) == id_elem and op(b, a) == id_elem:
                has_inv = True
                break
        if not has_inv: return False
    return True

def lists_equal(l1, l2):
    for x in l1:
        if x not in l2: return False
    for x in l2:
        if x not in l1: return False
    def unique_count(l):
        uniq = []
        for x in l:
            if x not in uniq:
                uniq.append(x)
        return len(uniq)
    return unique_count(l1) == unique_count(l2)

def conditions(witness):
    try:
        N_elems, H_elems, phi, op_N, op_H = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    h1_ok = False
    try:
        if is_group(H_elems, op_H):
            h1_ok = True
            for h in H_elems:
                mapped = []
                for n in N_elems:
                    pn = apply_phi(phi, h, n)
                    if pn not in N_elems: 
                        h1_ok = False
                        break
                    mapped.append(pn)
                if not h1_ok: break
                
                for n in N_elems:
                    if n not in mapped:
                        h1_ok = False
                        break
                if not h1_ok: break
                
                for n in N_elems:
                    for m in N_elems:
                        if apply_phi(phi, h, op_N(n, m)) != op_N(apply_phi(phi, h, n), apply_phi(phi, h, m)):
                            h1_ok = False
                            break
                    if not h1_ok: break
                if not h1_ok: break
                
            if h1_ok:
                for h in H_elems:
                    for k in H_elems:
                        hk = op_H(h, k)
                        for n in N_elems:
                            if apply_phi(phi, hk, n) != apply_phi(phi, h, apply_phi(phi, k, n)):
                                h1_ok = False
                                break
                        if not h1_ok: break
                    if not h1_ok: break
    except Exception:
        h1_ok = False

    h2_ok = h1_ok

    neg_q = False
    try:
        id_H = find_identity(H_elems, op_H)
        if id_H is not None:
            G_elems = [(n, h) for n in N_elems for h in H_elems]
            def op_G(x, y):
                n1, h1 = x
                n2, h2 = y
                return (op_N(n1, apply_phi(phi, h1, n2)), op_H(h1, h2))
                
            Z_G = []
            for g in G_elems:
                is_center = True
                for x in G_elems:
                    if op_G(g, x) != op_G(x, g):
                        is_center = False
                        break
                if is_center:
                    Z_G.append(g)
                    
            S1 = [g for g in Z_G if g[1] == id_H]
            
            Z_N = []
            for n in N_elems:
                is_center = True
                for m in N_elems:
                    if op_N(n, m) != op_N(m, n):
                        is_center = False
                        break
                if is_center:
                    Z_N.append(n)
                    
            S2 = []
            for n in Z_N:
                fixed_by_all = True
                for h in H_elems:
                    if apply_phi(phi, h, n) != n:
                        fixed_by_all = False
                        break
                if fixed_by_all:
                    S2.append((n, id_H))
                    
            neg_q = not lists_equal(S1, S2)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "H_2: G is the external semidirect product of N and H",
    "¬Q: Z(G) intersection (N x {1_H}) is not equal to the specified set"
]

N_HYP = 2
NEG_Q_INDEX = 2