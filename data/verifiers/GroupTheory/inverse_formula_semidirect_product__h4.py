import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            N = witness['N']
            H = witness['H']
            op_N = witness['op_N']
            op_H = witness['op_H']
            inv_N = witness['inv_N']
            inv_H = witness['inv_H']
            id_N = witness['id_N']
            id_H = witness['id_H']
            phi = witness['phi']
            G = witness.get('G')
            op_G = witness.get('op_G')
            inv_G = witness.get('inv_G')
            id_G = witness.get('id_G')
        else:
            N = witness.N
            H = witness.H
            op_N = witness.op_N
            op_H = witness.op_H
            inv_N = witness.inv_N
            inv_H = witness.inv_H
            id_N = witness.id_N
            id_H = witness.id_H
            phi = witness.phi
            G = getattr(witness, 'G', None)
            op_G = getattr(witness, 'op_G', None)
            inv_G = getattr(witness, 'inv_G', None)
            id_G = getattr(witness, 'id_G', None)
    except Exception:
        return [False, False, False, False]

    def is_group(G_set, op, inv, id_elem):
        if id_elem not in G_set: return False
        for a in G_set:
            if op(a, id_elem) != a or op(id_elem, a) != a: return False
            if op(a, inv(a)) != id_elem or op(inv(a), a) != id_elem: return False
            for b in G_set:
                ab = op(a, b)
                if ab not in G_set: return False
                for c in G_set:
                    if op(ab, c) != op(a, op(b, c)): return False
        return True

    try:
        h1 = is_group(N, op_N, inv_N, id_N) and is_group(H, op_H, inv_H, id_H)
    except Exception:
        h1 = False

    try:
        h2 = True
        for h in H:
            img = []
            for n in N:
                pn = phi(h, n)
                if pn not in N:
                    h2 = False
                    break
                img.append(pn)
            if not h2: break
            
            img_unique = []
            for x in img:
                if x not in img_unique:
                    img_unique.append(x)
            if len(img_unique) != len(N):
                h2 = False
                break
                
            for n1 in N:
                for n2 in N:
                    if phi(h, op_N(n1, n2)) != op_N(phi(h, n1), phi(h, n2)):
                        h2 = False
                        break
                if not h2: break
            if not h2: break
            
        if h2:
            for h1_elem in H:
                for h2_elem in H:
                    h1h2 = op_H(h1_elem, h2_elem)
                    for n in N:
                        if phi(h1h2, n) != phi(h1_elem, phi(h2_elem, n)):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    try:
        if G is None:
            h3 = True
            G_set = [(n, h) for n in N for h in H]
            id_G_val = (id_N, id_H)
            def op_G_val(x, y):
                n1, h1 = x
                n2, h2 = y
                return (op_N(n1, phi(h1, n2)), op_H(h1, h2))
        else:
            h3 = is_group(G, op_G, inv_G, id_G)
            if h3:
                expected_G = [(n, h) for n in N for h in H]
                if len(G) != len(expected_G):
                    h3 = False
                else:
                    for elem in expected_G:
                        if elem not in G:
                            h3 = False
                            break
                    if h3:
                        for n1 in N:
                            for h1 in H:
                                for n2 in N:
                                    for h2 in H:
                                        if op_G((n1, h1), (n2, h2)) != (op_N(n1, phi(h1, n2)), op_H(h1, h2)):
                                            h3 = False
                                            break
                                    if not h3: break
                                if not h3: break
                            if not h3: break
            G_set = G
            id_G_val = id_G
            op_G_val = op_G
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2 and h3:
            for n in N:
                for h in H:
                    expected_inv = (phi(inv_H(h), inv_N(n)), inv_H(h))
                    actual_inv = None
                    for x in G_set:
                        if op_G_val((n, h), x) == id_G_val and op_G_val(x, (n, h)) == id_G_val:
                            actual_inv = x
                            break
                    if actual_inv != expected_inv:
                        neg_q = True
                        break
                if neg_q: break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "H_3: G = N rtimes_phi H is the external semidirect product of N and H",
    "¬Q: The inverse of (n, h) in G is NOT (phi_{h^{-1}}(n^{-1}), h^{-1})"
]

N_HYP = 3
NEG_Q_INDEX = 3