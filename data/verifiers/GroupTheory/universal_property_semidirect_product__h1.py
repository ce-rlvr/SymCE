import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    # H1: G = N \rtimes_\phi H is the external semidirect product
    try:
        h1_ok = True
        if not witness.N or not witness.H:
            h1_ok = False
            
        if h1_ok:
            for n1 in witness.N:
                for n2 in witness.N:
                    if witness.mul_N(n1, n2) not in witness.N: h1_ok = False
        if h1_ok:
            for n1 in witness.N:
                for n2 in witness.N:
                    for n3 in witness.N:
                        if witness.mul_N(witness.mul_N(n1, n2), n3) != witness.mul_N(n1, witness.mul_N(n2, n3)):
                            h1_ok = False
        if h1_ok:
            for n in witness.N:
                if witness.mul_N(witness.id_N, n) != n or witness.mul_N(n, witness.id_N) != n:
                    h1_ok = False
        if h1_ok:
            for n in witness.N:
                inv = witness.inv_N(n)
                if witness.mul_N(n, inv) != witness.id_N or witness.mul_N(inv, n) != witness.id_N:
                    h1_ok = False
                    
        if h1_ok:
            for h1 in witness.H:
                for h2 in witness.H:
                    if witness.mul_H(h1, h2) not in witness.H: h1_ok = False
        if h1_ok:
            for h1 in witness.H:
                for h2 in witness.H:
                    for h3 in witness.H:
                        if witness.mul_H(witness.mul_H(h1, h2), h3) != witness.mul_H(h1, witness.mul_H(h2, h3)):
                            h1_ok = False
        if h1_ok:
            for h in witness.H:
                if witness.mul_H(witness.id_H, h) != h or witness.mul_H(h, witness.id_H) != h:
                    h1_ok = False
        if h1_ok:
            for h in witness.H:
                inv = witness.inv_H(h)
                if witness.mul_H(h, inv) != witness.id_H or witness.mul_H(inv, h) != witness.id_H:
                    h1_ok = False

        if h1_ok:
            for h in witness.H:
                for n in witness.N:
                    if witness.phi(h, n) not in witness.N:
                        h1_ok = False
    except Exception:
        h1_ok = False

    # H2: K is a group
    try:
        h2_ok = True
        if not witness.K:
            h2_ok = False
        if h2_ok:
            for k1 in witness.K:
                for k2 in witness.K:
                    if witness.mul_K(k1, k2) not in witness.K:
                        h2_ok = False
        if h2_ok:
            for k1 in witness.K:
                for k2 in witness.K:
                    for k3 in witness.K:
                        if witness.mul_K(witness.mul_K(k1, k2), k3) != witness.mul_K(k1, witness.mul_K(k2, k3)):
                            h2_ok = False
        if h2_ok:
            for k in witness.K:
                if witness.mul_K(witness.id_K, k) != k or witness.mul_K(k, witness.id_K) != k:
                    h2_ok = False
        if h2_ok:
            for k in witness.K:
                inv = witness.inv_K(k)
                if witness.mul_K(k, inv) != witness.id_K or witness.mul_K(inv, k) != witness.id_K:
                    h2_ok = False
    except Exception:
        h2_ok = False

    # H3: f: N -> K and g: H -> K are group homomorphisms
    try:
        h3_ok = True
        for n1 in witness.N:
            for n2 in witness.N:
                if witness.f(witness.mul_N(n1, n2)) != witness.mul_K(witness.f(n1), witness.f(n2)):
                    h3_ok = False
        for h1 in witness.H:
            for h2 in witness.H:
                if witness.g(witness.mul_H(h1, h2)) != witness.mul_K(witness.g(h1), witness.g(h2)):
                    h3_ok = False
    except Exception:
        h3_ok = False

    # H4: f(N) is normalized by g(H) in K
    try:
        h4_ok = True
        f_N = [witness.f(n) for n in witness.N]
        for h in witness.H:
            gh = witness.g(h)
            gh_inv = witness.inv_K(gh)
            for fn in f_N:
                conj = witness.mul_K(witness.mul_K(gh, fn), gh_inv)
                if conj not in f_N:
                    h4_ok = False
    except Exception:
        h4_ok = False

    # H5: f(phi_h(n)) = g(h) f(n) g(h)^{-1} for all n in N and h in H
    try:
        h5_ok = True
        for h in witness.H:
            gh = witness.g(h)
            gh_inv = witness.inv_K(gh)
            for n in witness.N:
                left = witness.f(witness.phi(h, n))
                right = witness.mul_K(witness.mul_K(gh, witness.f(n)), gh_inv)
                if left != right:
                    h5_ok = False
    except Exception:
        h5_ok = False

    # neg_Q: The conclusion fails
    try:
        G = [(n, h) for n in witness.N for h in witness.H]
        def mul_G(x, y):
            n1, h1 = x
            n2, h2 = y
            return (witness.mul_N(n1, witness.phi(h1, n2)), witness.mul_H(h1, h2))
        
        is_group = True
        for x in G:
            for y in G:
                if mul_G(x, y) not in G:
                    is_group = False
        
        if is_group:
            for x in G:
                for y in G:
                    for z in G:
                        if mul_G(mul_G(x, y), z) != mul_G(x, mul_G(y, z)):
                            is_group = False
                            break
                    if not is_group: break
                if not is_group: break
        
        if is_group:
            has_identity = False
            for e in G:
                is_id = True
                for x in G:
                    if mul_G(e, x) != x or mul_G(x, e) != x:
                        is_id = False
                        break
                if is_id:
                    has_identity = True
                    id_G = e
                    break
            if not has_identity:
                is_group = False
        
        if is_group:
            for x in G:
                has_inv = False
                for y in G:
                    if mul_G(x, y) == id_G and mul_G(y, x) == id_G:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break

        def Phi(x):
            n, h = x
            return witness.mul_K(witness.f(n), witness.g(h))
        
        is_hom = True
        for x in G:
            for y in G:
                if Phi(mul_G(x, y)) != witness.mul_K(Phi(x), Phi(y)):
                    is_hom = False
                    break
            if not is_hom: break
        
        neg_Q = not (is_group and is_hom)
    except Exception:
        neg_Q = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, h5_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: G = N \\rtimes_\\phi H is the external semidirect product",
    "H_2: K is a group",
    "H_3: f: N \\to K and g: H \\to K are group homomorphisms",
    "H_4: f(N) is normalized by g(H) in K",
    "H_5: f(\\phi_h(n)) = g(h) f(n) g(h)^{-1} for all n \\in N and h \\in H",
    "¬Q: There is no unique group homomorphism Phi: G -> K such that Phi((n, 1_H)) = f(n) and Phi((1_N, h)) = g(h)"
]

N_HYP = 5
NEG_Q_INDEX = 5